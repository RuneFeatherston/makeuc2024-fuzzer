# master/fuzzing_script.py
import logging
from scapy.all import IP, TCP, send

# Setup logging
logging.basicConfig(filename='/app/logs/fuzzing.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Target server information (update with actual IPs in a real setup)
TARGET_IPS = {
    "http_server": "http_server",  # DNS name as per docker-compose service name
    "ftp_server": "ftp_server"
}
TARGET_PORTS = {
    "http_server": 80,  # HTTP port
    "ftp_server": 21    # FTP port
}


def fuzz_http_server():
    packet = IP(dst=TARGET_IPS["http_server"]) / TCP(dport=TARGET_PORTS["http_server"], flags="S")
    send(packet)
    logging.info(f"Sent SYN packet to HTTP server at {TARGET_IPS['http_server']}:{TARGET_PORT}")
def fuzz_ftp_server():
    packet = IP(dst=TARGET_IPS["ftp_server"]) / TCP(dport=TARGET_PORTS["ftp_server"], flags="S")
    send(packet)
    logging.info(f"Sent SYN packet to FTP server at {TARGET_IPS['ftp_server']}:{TARGET_PORTS['ftp_server']}")


# Run fuzzing functions
# TODO: Define packet manipulation functions to allow for bit-wise fuzzing
# TODO: Implement logging such that successful crashes dump to logs
fuzz_http_server()
fuzz_ftp_server()
