import docker.errors
import requests, docker, sys, csv, json, os
import ContainerManager
from ContainerManager import *
#https://github.com/ollama/ollama/blob/main/docs/api.md
# from https://github.com/FrederickBerndt/LLMClient

#%% DEFINE LLM CLASS INTERFACE
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
        h = { "Content-Type": "application/json", "User-Agent": "MyUA"}
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
#%% Configuring Ollama

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
    
#%% USING THE LLM
def analyze_review(llm, review_text, categories):
    prompt = (
        f"Given the following review: '{review_text}', identify the best match "
        f"from the following categories: {', '.join(categories)}. "
        f"If no category matches, return 'n.a.'."
        f"Reply with only the matching category value or 'n.a.'."
    )
    try:
        return llm(prompt)
    except requests.exceptions.RequestException as e:
        print(f"Error querying Ollama: {e}")
        return "n.a."

if __name__ == "__main__":
    # update_ollama()
    ContainerManager.create_and_start_container("ollama_container")
    create_model("Mario", "MarioModel.txt")
    # start_container("ollama_container")
    Mario = LLMInstance("Mario")
    """ USE CASE: SENTIMENT ANALYSIS
    data = pandas.DataFrame(pandas.read_csv("data/apps.csv"))
    categories = ["positive", "neutral", "negative"]
    data["category"] = data["text"].apply(ArithmeticError
        lambda entry: analyze_review(llama3, entry, categories)
    )
    print(data.head())"""

    """ USE CASE: CHAT WITH MARIO """
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
