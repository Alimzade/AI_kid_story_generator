import os
from dotenv import load_dotenv
import requests

def filter_input(system_prompt):
    moderation_system_prompt = (
        "You are a content moderator for children's stories. Your task is to review the following prompt for harmful, inappropriate, or non-child-friendly content. "
        "Additionally, identify and remove any repetitive or overused phrases that might make the story less engaging for children. "
        "If any issues are found, please clean the prompt and return a safe and engaging version. add in the final prompt to Avoid starting the story with phrases like 'Once upon a time.' "
        "If the prompt is already appropriate and engaging, return it as is. add in the final prompt to  Avoid starting the story with phrases like 'Once upon a time."
    )

    user_prompt = f"Prompt: {system_prompt}"

    payload = {
        "model": "Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": moderation_system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.0
    }

    load_dotenv()
    api_url = os.getenv("API_URL")
    api_key = os.getenv("API_KEY")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()
        choices = result.get('choices', [])
        if choices:
            content = choices[0].get('message', {}).get('content', "")
            cleaned_prompt_section = content.split("Prompt:")[1].strip() if "Prompt:" in content else content.strip()
            return cleaned_prompt_section
        else:
            return system_prompt  # Return the original prompt if no choices found
    except requests.RequestException as e:
        return system_prompt  # Return the original prompt if there was an error
