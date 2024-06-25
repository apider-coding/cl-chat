# cl-chat

This is a streaming chat app using chainlit and local [ollama](https://ollama.ai) as default for inference backend. 

Any OpenAI API compatible backend can be used instead of ollama.


### Environment variables
- `OPENAI_API_URL` - The backend to use, default value is: `http://localhost:11434/v1`
- If running in docker desktop (locally) use `OPENAI_API_URL` = `http://host.docker.internal:11434/v1`
- `OPENAI_API_KEY` - The API key to use, default value is: `no-key`
- `MODEL` -  The model to use, default value is: `llama3:8b-instruct-q6_K`
- `MODEL_TEMPERATURE` - The temperature to use, default value is: `0.7`

## Run it
#### Prereqs
- Install [ollama](https://ollama.com/download)
- Pull whatever model you want or use suggested: 
```bash
ollama pull llama3:8b-instruct-q6_K
```

### locally
Install requirements:
```bash
pip install -r requirements.txt
```

Start GUI:
```bash
chainlit run cl-chat.py
```

Access the app on: http://localhost:8000/

### with docker
Build the container image

```bash
docker build -t cl-chat .
```

Run the container
```bash
docker run -d \
  --name cl-chat \
  -e OPENAI_API_URL='http://host.docker.internal:11434/v1' \
  -e OPENAI_API_KEY='no-key' \
  -e MODEL='llama3:8b-instruct-q6_K' \
  -p 8000:8000 cl-chat
```

Access the app on: http://localhost:8000/

#### Or pull the image from dockerhub
```bash
docker run -d \
  --name cl-chat \
  -e OPENAI_API_URL='http://host.docker.internal:11434/v1' \
  -e OPENAI_API_KEY='no-key' \
  -e MODEL='llama3:8b-instruct-q6_K' \
  -e MODEL_TEMPERATURE='0.5' \
  -p 8000:8000 apider/cl-chat:latest
```
