import docker
import logging
import time

# Initialize Docker client
client = docker.from_env()

# Configure logging to write to the master log file
logging.basicConfig(filename='/shared/logs/master_log.log', level=logging.INFO)

# Define constants
TARGET_CONTAINER_NAME = 'http_server'

def monitor_container():
    """Monitors Docker events and logs crashes for target containers."""
    try:
        for event in client.events(decode=True):
            # Check if the event is a container crash
            if event['Type'] == 'container' and event['Action'] == 'die':
                container_name = event['Actor']['Attributes'].get('name')
                if container_name == TARGET_CONTAINER_NAME:
                    crash_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    logging.info(f"{crash_time} - Container {container_name} crashed.")
                    logging.info(f"Crash detected for {container_name}.\n")
    except docker.DockerException as e:
        logging.error(f"Error while monitoring Docker events: {str(e)}")

# Start monitoring the container for crashes
monitor_container()
