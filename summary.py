import os
import requests
from dotenv import load_dotenv

def summarize_text(text: str) -> str:
    """
    Summarizes the provided text using an LLM model.
    """
    system_prompt = "You are a summarizer. Summarize the following story in a few sentences."

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        "temperature": 0.5,
        "max_tokens": 150
    }

    load_dotenv()
    api_url = os.getenv("API_URL")
    api_key = os.getenv("API_KEY")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        story_data = response.json()

        # Extract and return the content of the first choice if it exists
        choices = story_data.get('choices', [])
        if choices:
            first_choice = choices[0]
            message = first_choice.get('message', {})
            return message.get('content', "No content found in the response.")
        else:
            return "No choices found in the response."

    except requests.RequestException as e:
        # Handle request errors
        return f"Request failed with error: {str(e)}"