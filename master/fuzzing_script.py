import logging
from scapy.all import IP, TCP, send
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

# Fuzzing functions
def fuzz_http_server():
    if TARGET_IPS["http_server"]:
        packet = IP(dst=TARGET_IPS["http_server"]) / TCP(dport=TARGET_PORTS["http_server"], flags="S")
        send(packet)
        logging.info(f"Sent SYN packet to HTTP server at {TARGET_IPS['http_server']}:{TARGET_PORTS['http_server']}")

def fuzz_ftp_server():
    if TARGET_IPS["ftp_server"]:
        packet = IP(dst=TARGET_IPS["ftp_server"]) / TCP(dport=TARGET_PORTS["ftp_server"], flags="S")
        send(packet)
        logging.info(f"Sent SYN packet to FTP server at {TARGET_IPS['ftp_server']}:{TARGET_PORTS['ftp_server']}")

# Run fuzzing functions
fuzz_http_server()
fuzz_ftp_server()
