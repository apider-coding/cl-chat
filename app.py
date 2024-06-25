from openai import AsyncOpenAI
import chainlit as cl
import os

OPENAI_API_URL = os.getenv(
    # If running in docker use "host.docker.internal"
    'OPENAPI_URL', "http://host.docker.internal:11434/v1")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', "no-key")
MODEL = os.getenv('MODEL', "llama3:8b-instruct-q6_K")


client = AsyncOpenAI(base_url=OPENAI_API_URL, api_key=OPENAI_API_KEY, )
cl.instrument_openai()

settings = {
    "model": MODEL,
    # "temperature": 0.7,
    # "max_tokens": 500,
    # "top_p": 1,
    # "frequency_penalty": 0,
    # "presence_penalty": 0,
}


@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )


@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **settings
    )

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
