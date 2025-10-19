import os
import json
import re
import requests
from dotenv import load_dotenv

load_dotenv()
MISTRAL_API_KEY = os.getenv("LLM_API_KEY")

def log_info(msg): print(f"[INFO] {msg}")
def log_debug(msg): print(f"[DEBUG] {msg}")
def log_error(msg): print(f"[ERROR] {msg}")

def parse_task(task: str) -> dict:
    log_info(f"Parsing task: {task}")
    prompt = f"""You are a browser automation agent. Given a user task, output a JSON plan of browser actions.Respond ONLY with valid JSON
You must follow these rules:

1. Each action must be one of the following types :
   - "goto"
   - "wait"
   - "search"
   - "click"

2. Each action must use only the allowed keys:
   - "type" (always required)
   - "url" → only for "goto"
   - "selector" → only for "text" and "click"
   - "text" → only for "text"
   - "duration" → only for "wait" (in seconds)

Task: "{task}"

Respond with JSON like:
{{
  "actions": [
    {{"type": "goto", "url": "https://mail.google.com"}},
    {{"type": "search", "selector": "input[name='q']", "text": "label:promotions is:unread older_than:3m"}},
    {{"type": "click", "selector": "button[type='submit']"}}
  ]
}}"""

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-medium", 
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }

    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers=headers,
        data=json.dumps(payload)
    )

    try:
        response = requests.post(
            url="https://api.mistral.ai/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        print("🔍 Full LLM response:", response.json())
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        log_debug(f"LLM response: {content}")
        cleaned = re.sub(r"^```(?:json)?\n|\n```$", "", content.strip())
        print("LLM raw response:", content)

        return json.loads(cleaned)
    except Exception as e:
        log_error(f"LLM parsing failed: {e}")
        raise


