# LLMClient
						Prepare Execution

Dependency Management via Pip (when standard Python is used)
- make sure pip is registed as environmental-variable
    - C:\Users\Frederick\AppData\Local\Programs\Python\Python310
- Option 1: Load all Dependencies with "pip install dep1 dep2 dep3"
- Option 2: requires pip-tools ("pip install pip-tools")
    - When dependencies where changed: enter dependency in requirements.in file
    - compile requirements file: "pip-compile requirements.in"
    - install via requirements: "pip install -r requirements.txt"

Dependency Management via Conda (when Python was loaded with Anaconda/When scipt is executed in Anaconda Env)
- make sure conda is registered as environmental-variable
    C:\Users\ZEDATACCOUNDNAME\AppData\Local\anaconda3
    C:\Users\ZEDATACCOUNDNAME\AppData\Local\anaconda3\Scripts
    C:\Users\ZEDATACCOUNDNAME\AppData\Local\anaconda3\condabin
- use conda env update --file env.yaml"


                        Execute by Script

TIPS: only use conda environments (base environment) to avoid version conflicts (create custom environment if necessary)
1. start docker desktop
2. run script and prompt in console


						Manual Execution

1. pull ollama image: docker pull ollama/ollama
2. start docker container: docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
3. run (llama2) LLM. docker exec -it ollama ollama run llama2
	or in the docker shell: ollama run llama2
