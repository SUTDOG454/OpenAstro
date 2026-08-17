import os
from typing import Any, Dict, Optional

import requests

try:
    from dotenv import load_dotenv
except ImportError:  # Optional convenience dependency; environment variables remain sufficient.
    def load_dotenv() -> bool:
        return False

load_dotenv()  # Optional: loads .env in the working directory when python-dotenv is installed.

API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.ai/v1/search")


def _get_api_key(env_key: Optional[str] = None) -> str:
    key = env_key or os.getenv("DEEPSEEK_API_KEY")
    if not key:
        raise RuntimeError("Missing DEEPSEEK_API_KEY environment variable.")
    return key


def search_deepseek(query: str, *, api_key: Optional[str] = None, timeout: int = 10) -> Dict[str, Any]:
    """
    Perform a Deepseek search. API key is read from `DEEPSEEK_API_KEY` env var by default.

    Do not hardcode the key in source. For tests, pass `api_key` or mock requests.Session.
    """
    key = _get_api_key(api_key)
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    payload = {"query": query, "limit": 10}

    try:
        with requests.Session() as s:
            resp = s.post(API_URL, json=payload, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
    except requests.exceptions.RequestException as exc:
        # Never include the API key in logs or error messages
        raise RuntimeError("Deepseek request failed") from exc


if __name__ == "__main__":
    # Quick smoke run (requires DEEPSEEK_API_KEY env var)
    print(search_deepseek("example query"))
