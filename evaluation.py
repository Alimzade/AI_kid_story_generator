import os
from dotenv import load_dotenv
import requests
import textstat

def evaluate_options(story, data):
    results = {}
    results["protagonist_name"] = '✔️' if data["protagonistName"] in story else '❌'
    results["story_theme"] = '✔️' if data["storyTheme"].lower() in story.lower() else '❌'
    if data["friendName"]:
        results["friend_name"] = '✔️' if data["friendName"] in story else '❌'
    if data["educationalContent"]:
        results["educational_content"] = '✔️' if data["educationalContent"].lower() in story.lower() else '❌'

    all_passed = all(value == '✔️' for value in results.values())
    return {"options_evaluations": (all_passed, results)}

def evaluate_length(story, expected_length):
    passed = True
    word_count = len(story.split())
    if expected_length == "short":
        passed = word_count < 250
    elif expected_length == "medium":
        passed = 250 <= word_count <= 500
    elif expected_length == "long":
        passed = word_count > 500

    return {"length_evaluation": ('✔️' if passed else '❌', word_count)}

def evaluate_readability(story, age_group):
    flesch_score = textstat.flesch_reading_ease(story)
    flesch_grade = textstat.flesch_kincaid_grade(story)

    appropriate = None
    if age_group == "0-2":
        appropriate = flesch_grade <= 2 and flesch_score >= 90
    elif age_group == "2-4":
        appropriate = 2 < flesch_grade <= 4 and 85 <= flesch_score < 90
    elif age_group == "4-6":
        appropriate = 4 < flesch_grade <= 6 and 80 <= flesch_score < 90
    elif age_group == "6-9":
        appropriate = 6 < flesch_grade <= 9 and 75 <= flesch_score < 85
    elif not age_group:
        appropriate = None

    score_color = "green" if appropriate else "red"
    return {
        "readability_evaluation": {
            "flesch_score": flesch_score,
            "flesch_grade": flesch_grade,
            "appropriate_for_age_group": appropriate,
            "score_color": score_color,
        }
    }

def check_for_harmful_content(story, age_group):
    system_prompt = (
        f"You are a content moderator for children's stories with the age group of {age_group}. "
        f"Your task is to check the following story for any inappropriate, harmful, or non-child-friendly content. "
        f"Provide the output in the following structured format:\n\n"
        f"Safe: [Yes/No]\n"
        f"Harmful Content Found: [Yes/No]\n"
        f"Details: [If harmful content is found, provide details about it.]\n"
    )

    user_prompt = f"Story: {story}"

    payload = {
        "model": "Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": system_prompt},
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

        story_data = response.json()

        choices = story_data.get('choices', [])
        if choices:
            first_choice = choices[0]
            message = first_choice.get('message', {})
            content = message.get('content', "No content found in the response.")
            harmful = "No harmful content" if "Harmful Content Found: No" in content else "Harmful content found"
            return {"evaluation": harmful, "content": content}
        else:
            return {"evaluation": "Evaluation Failed", "content": "No choices found in the response."}

    except requests.RequestException as e:
        return {"evaluation": "Evaluation Failed", "content": f"Request failed with error: {str(e)}"}
