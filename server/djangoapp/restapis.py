import requests
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv("backend_url", default="http://127.0.0.1:3030")
sentiment_analyzer_url = os.getenv("sentiment_analyzer_url", default="http://127.0.0.1:5050/")

# ✅ GET Request
def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        params = "?" + "&".join(f"{key}={value}" for key, value in kwargs.items())
    request_url = f"{backend_url}{endpoint}{params}"
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print(f"GET request failed: {e}")
        return None

# ✅ Analyze Sentiment - with URL encoding and fallback
def analyze_review_sentiments(text):
    try:
        encoded_text = urllib.parse.quote(text)
        request_url = sentiment_analyzer_url + "analyze/" + encoded_text
        response = requests.get(request_url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Sentiment analysis failed with status {response.status_code}")
            return {"label": "neutral"}  # fallback label
    except Exception as err:
        print(f"Unexpected error: {err}, {type(err)}")
        return {"label": "neutral"}  # fallback in case of error

# ✅ POST Review
def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        return response.json()
    except Exception as e:
        print(f"POST request failed: {e}")
        return {"status": "failed", "message": "Network exception occurred"}
