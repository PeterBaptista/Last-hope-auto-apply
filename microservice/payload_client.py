import requests
import os
import json

PAYLOAD_URL = os.getenv("PAYLOAD_URL", "http://localhost:3000")
PAYLOAD_API_KEY = os.getenv("PAYLOAD_API_KEY") # If needed for authenticated access

def create_job_vacancy(data):
    """
    Creates a new job vacancy in Payload CMS via the REST API.
    """
    url = f"{PAYLOAD_URL}/api/job-vacancies"
    headers = {
        "Content-Type": "application/json"
    }

    # If API Key is configured/needed, add Authorization header
    if PAYLOAD_API_KEY:
        headers["Authorization"] = f"users API-Key {PAYLOAD_API_KEY}"

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating job vacancy in Payload: {e}")
        if response is not None:
             print(f"Response content: {response.text}")
        return None
