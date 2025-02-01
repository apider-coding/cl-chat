from openai import AsyncOpenAI
import chainlit as cl
import os

OPENAI_API_URL = os.getenv(
    # If running in docker use: "http://host.docker.internal:11434/v1"
    'OPENAI_API_URL', "http://localhost:11434/v1")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', "no-key")
MODEL = os.getenv('MODEL', "deepseek-r1:1.5b-qwen-distill-fp16")
MODEL_TEMPERATURE = os.getenv('MODEL_TEMPERATURE', 0.7)

print('Parameters: OPENAI_API_URL:', OPENAI_API_URL,
      ', MODEL:', MODEL,
      ', MODEL_TEMPERATURE:', MODEL_TEMPERATURE)

client = AsyncOpenAI(base_url=OPENAI_API_URL, api_key=OPENAI_API_KEY)
cl.instrument_openai()

settings = {
    "model": MODEL,
    "temperature": float(MODEL_TEMPERATURE),
    # "max_tokens": 500,
    # "top_p": 1,
    # "frequency_penalty": 0,
    # "presence_penalty": 0,
}


@ cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )


@ cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    # Initialize the response stream
    response_stream = await client.chat.completions.create(
        messages=message_history,
        stream=True,
        **settings
    )

    async for part in response_stream:
        if token := part.choices[0].delta.content or "":
            # Stream the new token immediately to the message widget
            await msg.stream_token(token)
            # Update the displayed content with this token
            if msg.content is None:
                await cl.get_message(messageId=part.choices[0].message.id).content

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
