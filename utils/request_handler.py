import requests
import random
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
]

def get(url, retries=3, timeout=10):
    """Fetch a URL with retries and random user-agent."""
    for attempt in range(retries):
        try:
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                return response
        except requests.RequestException:
            time.sleep(2)
    return None
