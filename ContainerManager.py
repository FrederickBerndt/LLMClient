import docker.errors
import requests, docker, sys, csv, json, os
PORT = 11434

def update_ollama():
    client = docker.from_env()
    print("Pulling the latest Ollama image...")
    client.images.pull("ollama/ollama")

def remove_existing_container(name):
    client = docker.from_env()
    print(f"Removing any existing {name} container...")
    try:
        container = client.containers.get(name)
        container.remove(force=True)
        print(f"Existing container {name} removed.")
    except docker.errors.NotFound:
        print(f"No container named {name} found", file=sys.stderr)

def create_and_start_container(name):
    try:
        client = docker.from_env()
        print("Starting Ollama container")
        container = client.containers.run(
            "ollama/ollama",                        # Docker image name
            name=name,          
            ports={f'{PORT}/tcp': PORT},       
            restart_policy={"Name": "unless-stopped"},
            detach=True
        )
        print("Ollama container is running")
    except docker.errors.DockerException as e:
        print(f"An error occurred while interacting with Docker: {e}", file=sys.stderr)
        sys.exit(1)

def start_container(name):
    try:
        client = docker.from_env()
        print(f"Loading container {name}")
        client.containers.get(name).start()
        print(f"Started container {name}")
    except docker.errors.NotFound:
        print("No container named {name} found")
    except docker.errors.DockerException as e:
        print(f"An error occurred while interacting with Docker: {e}", file=sys.stderr)
        sys.exit(1)

def stop_container(name):
    try:
        client = docker.from_env()
        print(f"Attempting to stop {name}")
        client.containers.get(name).stop()
        print(f"Stopped container {name}")
    except docker.errors.NotFound:
        print(f"No container named {name} found")
    except docker.errors.DockerException as e:
        print(f"An error occurred while interacting with Docker: {e}", file=sys.stderr)
        sys.exit(1)

def init_conn():
    # use fabric to ssh onto server
    # check possiblity for physical authentication (e.g. Yubikey)
    pass
    