import docker.errors
import requests, docker, sys, csv, json, os
#https://github.com/ollama/ollama/blob/main/docs/api.md

PORT = 11434
class LLMInstance:
    def __init__(self, model_name, api_endpoint=f"http://localhost:{PORT}/api/generate", **kwargs):
        self.model_name = model_name
        self.api_endpoint = api_endpoint
        self.session = requests.Session()
        self.kwargs = {"temperature": 0.7, "n": 1, **kwargs}
        print(f"Initialized OLLAMA with model_name: {self.model_name}, api_endpoint: {self.api_endpoint}, kwargs: {self.kwargs}")

    def generate(self, question, **kwargs):
        output = ""
        payload = {"model": self.model_name, "prompt": question, "stream": False, **self.kwargs, **kwargs}
        h = { "Content-Type": "application/json"}
        with self.session.post(self.api_endpoint, headers=h, json=payload, stream=True) as r:
            if r.status_code == 200:
                for line in r.iter_lines():
                    # Decode each line that is not empty
                    if line:
                        j = json.loads(line.decode("utf-8"))  # Ensure decoding from bytes to string
                        output += j.get("response", "")
                        # Break if the 'done' flag is True
                        if j.get("done", True): break
            else: r.raise_for_status()
        return output.strip()
    
    def __call__(self, question, **kwargs):
        return self.generate(question, **kwargs)

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

def pull_model(model_name):
    url = f"http://localhost:{PORT}/api/pull"
    data = {
        "model": model_name
    }
    try:
        print(f"Attempting to load model: {model_name}...")
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Model {model_name} loaded successfully.")
            # optional print(response.text)
        else:
            print(f"Failed to load model {model_name}. Status code: {response.status_code}, Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while communicating with the Ollama API: {e}", file=sys.stderr)
        sys.exit(1)
        
def create_model(name, modelfile, modelfile_path=os.getcwd()):
    # see https://github.com/ollama/ollama/blob/main/docs/modelfile.md#from-required
    url = f"http://localhost:{PORT}/api/create"
    with open(modelfile, 'r') as file:
        content = file.read()
    data = {
        "model": name,
        "modelfile": content,
        #"path": modelfile_path
    }
    try:
        print(f"Attempting to create {name} from {modelfile}")
        response = requests.post(url, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while communicating with the Ollama API: {e}", file=sys.stderr)
        sys.exit(1)

def init_conn():
    # use fabric to ssh onto server
    # check possiblity for physical authentication (e.g. Yubikey)
    pass

if __name__ == "__main__":
    # update_ollama()
    create_and_start_container("ollama_container")
    create_model("Mario", "MarioModel.txt")
    # start_container("ollama_container")
    Mario = LLMInstance("Mario")
    try:
        while True:
            try:
                prompt = input("prompt: ") or "Who are you?" # default if input is empty string
                if prompt == "break": break
                resonse = Mario(prompt)
                print(resonse)
            except ValueError:
                print("Invalid prompt format")
    finally: stop_container("ollama_container")