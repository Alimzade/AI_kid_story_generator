import os
from dotenv import load_dotenv
import requests

from filter_inputs import filter_input


def generate_story(data, bullet_points=[]):
    protagonist_name = data.get("protagonistName")
    protagonist_gender = data.get("protagonistGender")
    story_theme = data.get("storyTheme")
    age_group = data.get("ageGroup")
    educational_content = data.get("educationalContent")
    friend_name = data.get("friendName")
    friend_gender = data.get("friendGender")
    story_description = data.get("storyDescription")
    story_length = data.get("storyLength")

    load_dotenv()
    api_url = os.getenv("API_URL")
    api_key = os.getenv("API_KEY")

    system_prompt = f"""
    - You are a story generator for children. Your task is to create fun, imaginative, and educational stories that are appropriate for young readers. First sentence should be fun!!
    - The protagonist's name is {protagonist_name}, who is {protagonist_gender}. If name is inapplicable for children's stories, please use a suitable name.
    """

    if friend_name:
        system_prompt += f" The protagonist has a friend named {friend_name}, who is {friend_gender}. If name is inapplicable for children's stories, please use a suitable name."
    if story_theme:
        system_prompt += f" The story theme is {story_theme}."
    if age_group:
        system_prompt += f" The story and used language simplicity MUST BE suitable for children aged {age_group}."
    if educational_content:
        system_prompt += f" The story should include an educational element about {educational_content}."
    if story_description:
        system_prompt += f" The story should be about {story_description}."
    if story_length == "short":
        system_prompt += f" The story should be a 50-250 words story."
    elif story_length == "medium":
        system_prompt += f" The story should be a 250-500 words story."
    elif story_length == "long":
        system_prompt += f" The story should VERY LONG and contain more than 700 words."

    if bullet_points:
        system_prompt += "\n- Additionally, the story should consider that user previously liked stories containing following key points:\n"
        for point in bullet_points:
            system_prompt += f" {point}"
    
    user_prompt = "Write a story with the above details. Do not write any Notes."

    # Filter the system prompt
    system_prompt = filter_input(system_prompt)

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.8,
        "max_tokens": 500 if story_length == "short" else 1000
    }

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    response = requests.post(api_url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        story = response.json()['choices'][0]['message']['content']
        return story
    else:
        return f"Request failed with status code {response.status_code}"