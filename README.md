# TestCaseLLM
## Setup
### Install required tools
#### 1) Install Docker
Download and install Docker Desktop: https://www.docker.com/get-started/

#### 2) Install and setup Ollama
Download and install Ollama: https://ollama.com/download \
Once Ollama has been installed pull the required models. 
```
ollama pull qwen3:14b
ollama pull embeddinggemma:300m
```
In the default setup we use the "qwen3:14b" llm model and the "embeddinggemma:300m" embeddings model.
**If you wish to use different models please specify them in the .env file.**

#### 3) Setup test requirements
Install the required packages for the test, the use of a virtual environment is recommended.
```
pip install --no-cache-dir -r test/requirements_test.txt
```

### Run agent
1) Make sure Docker Desktop is running
2) Make sure ollama is running: 
```
ollama serve
```
3) Start agent container:
```
 docker-compose up
```
4) The Policy Q&A Agent has a REST API interface, 
once the container is running the documentation of the API is available at: http://localhost:8000/docs
(assuming default settings)

### Evaluate agent
The agent can be evaluated using pytest as follows:
1) Make sure Docker Desktop is running
2) Make sure ollama is running: 
```
ollama serve
```
3) Run pytest:
```
pytest
```
_The test will spin up the container automatically._

## Architecture
![Alt text](architecture/architecture.png)

## Limitations and improvements