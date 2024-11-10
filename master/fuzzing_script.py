import logging
from scapy.all import IP, TCP, send
import docker
import time
import random
import socket
from evolve import init_pop, fitness, crossover, mutate
from utils import levenshtein_distance


# Initialize Docker client
client = docker.from_env()
TARGET_CONTAINER_NAME = "http_server"

# Set up logging for monitoring
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Function to resolve service names to IPs
def resolve_ip(service_name: str) -> str:
    """
    Args:
        service_name (str): The DNS name of the service to resolve.

    Returns:
        str or None: The resolved IP address as a string, or None if the
        resolution fails.
    """
    try:
        ip = socket.gethostbyname(service_name)
        logging.info(f"Resolved {service_name} to {ip}")
        return ip
    except socket.error as err:
        logging.error(f"Error resolving {service_name}: {err}")
        return None

def check_container():
    """Monitors Docker events and logs crashes for the target container."""
    try:
        logging.info("Checking Docker events once...")
        # Get the most recent Docker event related to the 'die' event
        event = next(client.events(decode=True, filters={'event': 'die'}), None)

        if event:
            # Check if the event is a container crash
            container_name = event['Actor']['Attributes'].get('name')

            # If this is the target container, log the crash
            if container_name == TARGET_CONTAINER_NAME:
                crash_time = time.strftime("%Y-%m-%d %H:%M:%S")
                logging.info(f"{crash_time} - Container {container_name} crashed.")
                return True  # Indicate a crash for the genetic algorithm loop
            else:
                logging.info(f"Received 'die' event for container {container_name}, but not target container.")
                return False
        else:
            logging.info("No Docker events found.")
            return False
    except docker.DockerException as e:
        logging.error(f"Error while monitoring Docker events: {str(e)}")
        return False

# Initialize population
logging.info("Initializing population...")
population = init_pop(pop_size=20)
logging.info(f"Population initialized with {len(population)} individuals.")

while True:
    # Evaluate fitness of population
    logging.info("Evaluating fitness of population...")
    fit_results = fitness(population)
    max_distance_payload = fit_results["max_distance_payload"]
    min_distance_payload = fit_results["min_distance_payload"]

    # Log fitness results
    logging.info(f"Max distance payload: {max_distance_payload}")
    logging.info(f"Min distance payload: {min_distance_payload}")

    parents = [max_distance_payload, min_distance_payload]

    # Crossover to create new population
    logging.info("Performing crossover to generate new population...")
    new_population = []
    for _ in range(len(population) // 2):
        father, mother = random.sample(parents, 2)
        new_population.extend(crossover(father, mother))

    # Mutate the new population
    logging.info("Performing mutation on new population...")
    mutated_population = [mutate(payload) for payload in new_population]

    # Send mutated payloads and check for server crash
    for payload in mutated_population:
        logging.info(f"Preparing to send payload: {payload}")

        # Resolve IP of the target server
        server_ip = resolve_ip("http_server")
        if not server_ip:
            logging.error("Unable to resolve target server IP. Skipping payload.")
            continue

        # Prepare packet
        packet = IP(dst=server_ip) / TCP(dport=8080) / payload

        # Send the packet
        logging.info(f"Sending packet with payload: {payload}")
        send(packet)

        # Check if the server crashed
        if check_container():
            logging.error(f"Server crashed with payload: {payload}")
            print(f"Payload that caused crash: {payload}")
            break  # End the loop if a crash is detected
