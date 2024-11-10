import docker
import logging
import time
from collections import deque
from datetime import datetime
import threading
import random
import string

# Initialize Docker client
client = docker.from_env()

# Configure logging to write to the master log file
logging.basicConfig(filename='/shared/logs/master_log.log', level=logging.INFO)

# Define constants
TARGET_CONTAINER_NAME = 'http_server'
CRASH_LOG_PATH = '/shared/logs/crash_report.log'
BUFFER_SIZE = 10  # Number of packets to hold in buffer
TIME_LIMIT = 10  # Time limit (in seconds) to keep old packets in the buffer
SIMULATION_INTERVAL = 0.1  # Reduced interval for full speed packet influx

# Initialize packet buffer to keep the last few packets (with timestamps)
packet_buffer = deque(maxlen=BUFFER_SIZE)

# Variable to control if the deque is frozen
is_buffer_frozen = False


class Packet:
    """Class to represent a network packet with its data and timestamp."""
    
    def __init__(self, packet_data):
        self.packet_data = packet_data
        self.timestamp = time.time()

    def __repr__(self):
        return f"Packet(data={self.packet_data}, timestamp={self.timestamp})"


def monitor_container():
    """Monitors Docker events and logs crashes for target containers."""
    global is_buffer_frozen
    try:
        for event in client.events(decode=True):
            # Check if the event is a container crash
            if event['Type'] == 'container' and event['Action'] == 'die':
                container_name = event['Actor']['Attributes'].get('name')
                if container_name == TARGET_CONTAINER_NAME:
                    crash_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    logging.info(f"{crash_time} - Container {container_name} crashed.")
                    
                    # Freeze the packet buffer
                    freeze_packet_buffer()
                    
                    # Log the packet most likely causing the crash
                    log_crash_details(crash_time)
    except docker.DockerException as e:
        logging.error(f"Error while monitoring Docker events: {str(e)}")


def freeze_packet_buffer():
    """Freezes the packet buffer and prevents further additions."""
    global is_buffer_frozen
    is_buffer_frozen = True


def add_packet_to_buffer(packet_data):
    """Adds a packet to the buffer with a timestamp for crash tracking."""
    if not is_buffer_frozen:
        packet = Packet(packet_data)  # Create a new Packet instance
        packet_buffer.append(packet)
    else:
        logging.info("Buffer is frozen. No more packets will be added.")


def log_crash_details(crash_time):
    """Logs crash details and the last packet sent before the crash."""
    # Retrieve the timestamp of the crash event
    crash_timestamp = datetime.strptime(crash_time, "%Y-%m-%d %H:%M:%S").timestamp()

    # Find the most recent packet that matches the crash time
    closest_packet = find_closest_packet(crash_timestamp)
    
    with open(CRASH_LOG_PATH, 'a') as crash_log:
        crash_log.write(f"Crash Time: {crash_time}\n")
        if closest_packet:
            crash_log.write(f"Most Likely Cause Packet:\n{closest_packet.packet_data}\n")
        else:
            crash_log.write("No matching packet found.\n")
        crash_log.write("\n")


def find_closest_packet(crash_timestamp):
    """Finds the packet with the closest timestamp to the crash event."""
    closest_packet = None
    min_time_diff = float('inf')
    
    # Iterate through all packets in the buffer (which are Packet objects)
    for packet in packet_buffer:
        time_diff = abs(crash_timestamp - packet.timestamp)
        if time_diff < min_time_diff:
            min_time_diff = time_diff
            closest_packet = packet
    
    return closest_packet


def cleanup_old_packets():
    """Cleans up packets older than the time limit from the buffer."""
    current_time = time.time()
    for packet in list(packet_buffer):
        if current_time - packet.timestamp > TIME_LIMIT:
            packet_buffer.remove(packet)
            logging.info(f"Removed old packet: {packet.packet_data}")


def generate_test_packet():
    """Generates a test packet with a unique label and adds it to the buffer."""
    # Adding randomness to packet name
    packet_name = "TEST_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return packet_name


def simulate_packet_flow():
    """Simulates a continuous flow of packets being added to the buffer at full speed."""
    while not is_buffer_frozen:
        packet = generate_test_packet()
        add_packet_to_buffer(packet)
        logging.info(f"Added packet: {packet}")
        time.sleep(SIMULATION_INTERVAL)  # Adjust to a minimal interval for full speed


# Start monitoring the container for crashes in a separate thread
monitor_thread = threading.Thread(target=monitor_container)
monitor_thread.daemon = True  # Allow the thread to exit when the main program ends
monitor_thread.start()

# Start simulating packet flow in a separate thread
simulation_thread = threading.Thread(target=simulate_packet_flow)
simulation_thread.daemon = True  # Allow the thread to exit when the main program ends
simulation_thread.start()

# Example: Periodic cleanup of old packets (could be called periodically from the main loop)
cleanup_thread = threading.Thread(target=cleanup_old_packets)
cleanup_thread.daemon = True
cleanup_thread.start()

# Keep the main program running to allow threads to continue executing
while True:
    time.sleep(1)
