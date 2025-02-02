import requests
from openai import AsyncOpenAI
import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider
import os


OPENAI_API_URL = os.getenv(
    # If running in docker use: "http://host.docker.internal:11434/v1"
    'OPENAI_API_URL', "http://localhost:11434/v1")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', "no-key")


def fetch_models():
    """Fetch available models."""
    url = f"{OPENAI_API_URL}/models"
    response = requests.get(url)
    if response.status_code == 200:
        r = response.json()
        model_list = []
        for model in r["data"]:
            model_list.append(model["id"])
        return model_list
    raise Exception()


# Get available models
try:
    models = fetch_models()
    print(f"Successfully fetched models from {
          OPENAI_API_URL}/models, Models count: {len(models)}")
except Exception as e:
    print(f"Error fetching models from {OPENAI_API_URL}/models")
    print(e)
    exit(1)

client = AsyncOpenAI(base_url=OPENAI_API_URL, api_key=OPENAI_API_KEY)
cl.instrument_openai()

message_history = []


@cl.on_chat_start
async def start():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )

    settings = await cl.ChatSettings(
        [
            Select(
                id="model",
                label="Model",
                values=models,
                initial_index=0,
            ),
            Slider(
                id="temperature",
                label="Model Temperature",
                initial=0.2,
                min=0,
                max=2,
                step=0.1,
            ),
        ]
    ).send()
    cl.user_session.set("settings", settings)
    await update_settings(settings)


@cl.on_settings_update
async def update_settings(settings):
    cl.user_session.set("settings", settings)
    print("Model settings updated:", settings)

    elements = [
        cl.Text(name=f"{settings['model']}",
                content=f"Temperature: {settings['temperature']}", display="inline")
    ]
    await cl.Message(
        content=f"Selected model & settings. ({len(models)} models available)",
        elements=elements,
    ).send()


@ cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})
    settings = cl.user_session.get("settings")
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
