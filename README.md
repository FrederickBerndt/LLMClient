# Prepare Execution

## Dependency Loading

### Using Pip (Standard Python)

Ensure that `pip` is registered as an environment variable. Typically, its path is:
```
C:\Users\Frederick\AppData\Local\Programs\Python\Python310
```

#### Option 1: Install Dependencies Directly
Use the following command to install all required dependencies:
```
pip install dep1 dep2 dep3
```

#### Option 2: Install Dependencies with `pip-tools`
`pip-tools` allows for better management of dependencies. To use it:
1. Install `pip-tools`:
   ```
   pip install pip-tools
   ```
2. When dependencies change:
   - Add the new dependency to the `requirements.in` file.
   - Compile the `requirements.txt` file:
     ```
     pip-compile requirements.in
     ```
3. Install dependencies from the compiled requirements file:
   ```
   pip install -r requirements.txt
   ```

### Using Conda (Anaconda Python)

Ensure that `conda` is registered as an environment variable. Typical paths include:
```
C:\Users\ZEDATACCOUNDNAME\AppData\Local\anaconda3
C:\Users\ZEDATACCOUNDNAME\AppData\Local\anaconda3\Scripts
C:\Users\ZEDATACCOUNDNAME\AppData\Local\anaconda3\condabin
```

To update the environment, use:
```
conda env update --file env.yaml
```

## Execution Guidelines

### Script Execution
**Tip:** Use conda environments (preferably the base environment) to avoid version conflicts. Create custom environments if necessary.

Steps:
1. Start Docker Desktop.
2. Run the script and prompt in the console.
3. to close the console and stop the container prompt "break"

### Manual Execution
1. Pull the required Docker image:
   ```
   docker pull ollama/ollama
   ```
2. Start the Docker container:
   ```
   docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
   ```
3. Run the LLM (e.g., Llama 2):
   - Directly from the host:
     ```
     docker exec -it ollama ollama run llama2
     ```
   - Or from within the Docker shell:
     ```
     ollama run llama2
     ```

