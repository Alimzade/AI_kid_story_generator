import os
import requests
from dotenv import load_dotenv

def extract_bullet_points(text: str) -> str:
    """
    Extracts bullet points from the provided text using an LLM model.
    """
    system_prompt = (
        "Analyze the following text to identify and extract the key features or preferences in short that describe what the user enjoys in a story. "
        "Present these preferences as a list of bullet points. Focus on elements such as themes, genres, character traits, or other details that reflect the user's taste."
        "Output expected to be quite SHORT and informative for future story generations."
    )

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        "temperature": 0.5,
        "max_tokens": 200
    }

    load_dotenv()
    api_url = os.getenv("API_URL")
    api_key = os.getenv("API_KEY")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  

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
        return f"Request failed with error: {str(e)}"