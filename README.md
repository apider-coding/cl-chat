# cl-chat

This is a streaming chat app using chainlit and ollama as backend. 

Any OpenAI API compatible backend can be used instead of Ollama.


### Environment variables
* `OPENAI_API_URL` - The backend to use, default value is: `http://localhost:11434/v1`
* If running in docker use `OPENAI_API_URL` = `http://host.docker.internal:11434/v1`
* `OPENAI_API_KEY` - The API key to use, default value is: `no-key`
* `MODEL` -  The model to use, default value is: `llama3:8b-instruct-q6_K`
* `MODEL_TEMPERATURE` - The temperature to use, default value is: `0.7`

### Usage
Install requirements:
```bash
pip install -r requirements.txt
```

Start GUI:
```bash
chainlit run cl-chat.py
```

Access the app on: http://localhost:8000/


