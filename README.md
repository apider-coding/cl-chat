# cl-chat

This is a streaming chat app using chainlit and local [ollama](https://ollama.ai) as default for inference backend. 

Any OpenAI API compatible backend can be used instead of ollama.


### Environment variables
- `OPENAI_API_URL` - The backend to use, default value is: `http://localhost:11434/v1` - If running in Docker Desktop use: `http://host.docker.internal:11434/v1`
- `OPENAI_API_KEY` - The API key to use, default value is: `no-key`
- `MODEL` -  The model to use, default value is: `deepseek-r1:1.5b-qwen-distill-fp16`
- `MODEL_TEMPERATURE` - The temperature to use, default value is: `0.5`

## Run it
#### Prereqs
- Install [ollama](https://ollama.com/download)
- Pull whatever model you want or use suggested: 
```bash
ollama pull deepseek-r1:1.5b-qwen-distill-fp16
```

### locally
Install requirements:
```bash
pip install -r requirements.txt
```

Start GUI:
```bash
chainlit run app.py
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
  -e MODEL='deepseek-r1:1.5b-qwen-distill-fp16' \
  -e MODEL_TEMPERATURE='0.5' \
  -p 8000:8000 cl-chat
```

Access the app on: http://localhost:8000/

#### Or pull the image from dockerhub
```bash
docker run -d \
  --name cl-chat \
  -e OPENAI_API_URL='http://host.docker.internal:11434/v1' \
  -e OPENAI_API_KEY='no-key' \
  -e MODEL='deepseek-r1:1.5b-qwen-distill-fp16' \
  -e MODEL_TEMPERATURE='0.5' \
  -p 8000:8000 apider/cl-chat:latest
```
