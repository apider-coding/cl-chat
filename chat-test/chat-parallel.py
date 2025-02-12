import asyncio
# import openai
# from openai import OpenAI
from openai import AsyncOpenAI
import time
import os
import sys

if len(sys.argv) < 3:
    print("Provide model as first and number of parallel request as second argument.")
    print(f"Example: {sys.argv[0]} modelname 8")
    exit(1)
MODEL = sys.argv[1]
REQUESTS = int(sys.argv[2])

# Make sure the API key is available as an environment variable.
openai_api_key = os.environ.get("OPENAI_API_KEY", "EMPTY")
# openai_api_base = "http://192.168.1.62:11434/v1"
# openai_api_base = "http://192.168.1.62:30000/v1"
# openai_api_base = "http://serv4.home:30000/v1"
openai_api_base = "http://serv4.home:11434/v1"
# openai_api_base = "http://host.docker.internal:30000/v1"

client = AsyncOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# models = client.models.list()
# model = models.data[0].id


# async def get_first_model_id():
#     # Asynchronously iterate through the paginator to get the first model
#     async for model in client.models.list():
#         return model.id
#     return None


async def fetch_completion(prompt: str, model_id: str):
    # Record the start time
    start_time = time.time()

    # Make an asynchronous API call.
    # Use acreate instead of create to enable asynchronous behavior.
    response = await client.chat.completions.create(
        model=model_id,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time (in seconds)
    duration = end_time - start_time

    # Extract token usage (assuming the response includes a 'usage' field)
    # For ChatCompletion responses, the usage field typically includes total_tokens.
    # token_usage = response["usage"]["total_tokens"]
    token_usage = response.usage.total_tokens

    # Calculate tokens per second
    tokens_per_sec = token_usage / duration if duration > 0 else 0
    return token_usage, duration, tokens_per_sec


async def main():
    model_id = MODEL

    # if model_id is None:
    #     print("No model found.")
    #     return

    print('URL: ', openai_api_base)
    print('Model:', model_id)
    print('Parallel Requests:', REQUESTS)
    # Define your prompt (you could vary the prompt if needed)
    # prompt = "Explain the concept of asynchronous programming."
    prompt = "Tell me a story about a fox."

    # Create a list of 32 asynchronous tasks to fetch responses concurrently
    tasks = [fetch_completion(prompt, model_id) for _ in range(REQUESTS)]

    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)

    # Print out the tokens used, elapsed time, and tokens per second for each response
    for idx, (tokens, duration, tps) in enumerate(results, start=1):
        print(f"Response {idx}: {tokens} tokens generated in {duration:.2f} seconds "
              f"({tps:.2f} tokens/sec)")

if __name__ == "__main__":
    asyncio.run(main())
