import requests
import json
import os

models = [
    ""
]

def get_openrouter_response_basic(prompt, model="", system_prompt=None, **kwargs):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set.")
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    data = json.dumps(
        {
            "model": model,
            "messages": messages
        }
    )
    print("Sending request to OpenRouter API...")
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        data=data
    )
    print("Received response from OpenRouter API.")
    if response.status_code == 200:
        return response
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")
    