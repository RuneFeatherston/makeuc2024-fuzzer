import logging
import random
from scapy.all import IP, TCP, send
from scapy.layers.inet import RandInt, RandShort
import socket
import sys

# Setup logging
logging.basicConfig(filename='/app/logs/fuzzing.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to resolve service names to IPs
def resolve_ip(service_name):
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

# Target server information (using resolved IPs)
TARGET_IPS = {
    "http_server": resolve_ip("http_server"),  # Resolve DNS name to IP
    "ftp_server": resolve_ip("ftp_server")    # Resolve DNS name to IP
}

# Check if both IPs were successfully resolved
if not TARGET_IPS["http_server"] or not TARGET_IPS["ftp_server"]:
    logging.error("One or more server IPs could not be resolved. Exiting script.")
    sys.exit(1)  # Exit the script if IP resolution fails

TARGET_PORTS = {
    "http_server": 80,  # HTTP port
    "ftp_server": 21    # FTP port
}

# Function to create a mutated packet with random fields
def create_mutated_packet(dst_ip, dst_port):
    packet = IP(dst=dst_ip) / TCP(dport=dst_port, flags="S")

    # Mutate TTL
    if random.choice([True, False]):
        packet[IP].ttl = random.randint(1, 255)

    # Mutate TCP flags
    if random.choice([True, False]):
        packet[TCP].flags = random.choice(["S", "A", "F", "P", "R", "U"])

    # Mutate TCP sequence number
    if random.choice([True, False]):
        packet[TCP].seq = RandInt()

    # Mutate source port
    if random.choice([True, False]):
        packet[TCP].sport = RandShort()

    return packet

# Fuzzing functions with mutation
def fuzz_http_server():
    if TARGET_IPS["http_server"]:
        mutated_packet = create_mutated_packet(TARGET_IPS["http_server"], TARGET_PORTS["http_server"])
        send(mutated_packet)
        packet_id = id(mutated_packet)
        logging.info(f"Packet ID {packet_id}: Sent mutated packet to HTTP server with TTL={mutated_packet[IP].ttl}, TCP Flags={mutated_packet[TCP].flags}, TCP Seq={mutated_packet[TCP].seq}, Source Port={mutated_packet[TCP].sport}")

def fuzz_ftp_server():
    if TARGET_IPS["ftp_server"]:
        mutated_packet = create_mutated_packet(TARGET_IPS["ftp_server"], TARGET_PORTS["ftp_server"])
        send(mutated_packet)
        packet_id = id(mutated_packet)
        logging.info(f"Packet ID {packet_id}: Sent mutated packet to FTP server with TTL={mutated_packet[IP].ttl}, TCP Flags={mutated_packet[TCP].flags}, TCP Seq={mutated_packet[TCP].seq}, Source Port={mutated_packet[TCP].sport}")

# Run fuzzing functions
fuzz_http_server()
fuzz_ftp_server()
