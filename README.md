# LLMClient
						Execute by Script
TIPS: only use conda environments (base environment) to avoid version conflicts (create custom environment if necessary)

1. register conda as environmental-variable
    C:\Users\ZEDATACCOUNDNAME\AppData\Local\anaconda3
    C:\Users\ZEDATACCOUNDNAME\AppData\Local\anaconda3\Scripts
    C:\Users\ZEDATACCOUNDNAME\AppData\Local\anaconda3\condabin
2. start docker desktop
3. use conda env update --file env.yaml
4. run script and prompt in console

						Manual Execution
1. pull ollama image: docker pull ollama/ollama
2. start docker container: docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
3. run (llama2) LLM. docker exec -it ollama ollama run llama2
	or in the docker shell: ollama run llama2
