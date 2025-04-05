# tinyurl_helper.py

import requests

# TinyURL API URL for shortening links
TINYURL_API_URL = "https://api.tinyurl.com/create"

def shorten_url(url):
    response = requests.get(f"{TINYURL_API_URL}?url={url}")
    if response.status_code == 200:
        return response.json().get("data", {}).get("url", url)
    else:
        print(f"Error shortening URL: {response.status_code}")
        return url