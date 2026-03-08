import os
import sys
import json
import requests
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

API_KEY = os.getenv("LLM_API_KEY")
model_name = "minimax-cn/MiniMax-M2.5"

import os
import sys
import json
import requests
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

API_KEY = os.getenv("LLM_API_KEY")
model_name = "minimax-cn/MiniMax-M2.5"

# Testing Anthropic format
headers = {
    "x-api-key": API_KEY,
    "anthropic-version": "2023-06-01",
    "Content-Type": "application/json"
}

payload = {
    "model": model_name,
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Hello, simply reply 'Hi'."}
    ]
}

print("Testing basic chat to https://api.minimaxi.com/anthropic/v1/messages ...")
resp = requests.post("https://api.minimaxi.com/anthropic/v1/messages", headers=headers, json=payload)
print(resp.status_code, resp.text)

print("\nTesting basic chat to https://api.minimaxi.com/v1/messages ...")
resp2 = requests.post("https://api.minimaxi.com/v1/messages", headers=headers, json=payload)
print(resp2.status_code, resp2.text)
