import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app  

client = TestClient(app)

@pytest.fixture
def mock_get_db():
    with patch('main.get_db') as mock:
        yield mock

@patch('main.generate_story')
@patch('main.summarize_text')
@patch('main.check_for_harmful_content')
@patch('main.evaluate_length')
@patch('main.evaluate_options')
@patch('main.evaluate_readability')
def test_generate_story(mock_evaluate_readability, mock_evaluate_options, mock_evaluate_length, mock_check_for_harmful_content, mock_summarize_text, mock_generate_story, mock_get_db):
    mock_generate_story.return_value = "Once upon a time..."
    mock_summarize_text.return_value = "Summary of the story."
    mock_check_for_harmful_content.return_value = {"evaluation": "Safe", "content": ""}
    mock_evaluate_length.return_value = {"length_evaluation": ('✔️', 200)}
    mock_evaluate_options.return_value = {"options_evaluations": (True, {'protagonist_name': '✔️', 'story_theme': '✔️'})}
    mock_evaluate_readability.return_value = {"readability_evaluation": {'flesch_score': 85, 'flesch_grade': 5, 'appropriate_for_age_group': True, 'score_color': 'green'}}
    
    response = client.post("/generate-story", data={
        "protagonistName": "Alex",
        "protagonistGender": "male",
        "storyTheme": "Adventure",
        "ageGroup": "5-7",
        "educationalContent": "Sharing",
        "friendName": "Jordan",
        "friendGender": "female",
        "storyDescription": "a great adventure",
        "storyLength": "short"
    })

    assert response.status_code == 200
    assert "Once upon a time..." in response.text

@patch('main.get_db')
@patch('main.generate_story')
def test_generate_story_db(mock_generate_story, mock_get_db):
    mock_generate_story.return_value = "Once upon a time..."
    
    response = client.post("/generate-story", data={
        "protagonistName": "Alex",
        "protagonistGender": "male",
        "storyTheme": "Adventure",
        "ageGroup": "5-7",
        "educationalContent": "Sharing",
        "friendName": "Jordan",
        "friendGender": "female",
        "storyDescription": "a great adventure",
        "storyLength": "short"
    })

    assert response.status_code == 200
    assert "Once upon a time..." in response.text

@patch('main.get_db')
def test_register(mock_get_db):
    mock_get_db.return_value = MagicMock()
    
    response = client.post("/register", data={
        "username": "testuser",
        "password": "testpass"
    })

    assert response.status_code == 303  

@patch('main.get_db')
def test_login(mock_get_db):
    # Mocking DB session and user authentication
    mock_get_db.return_value = MagicMock()
    with patch('main.authenticate_user') as mock_authenticate_user:
        mock_authenticate_user.return_value = True
        response = client.post("/login", data={
            "username": "testuser",
            "password": "testpass"
        })

        assert response.status_code == 303  

@patch('main.get_db')
def test_past_stories(mock_get_db):
    mock_get_db.return_value = MagicMock()
    
    response = client.get("/past-stories")

    assert response.status_code == 200
    assert "Past Stories" in response.text

@patch('main.get_db')
def test_favorites(mock_get_db):
    mock_get_db.return_value = MagicMock()
    
    response = client.get("/favorites")

    assert response.status_code == 200
    assert "Favorites" in response.text

if __name__ == "__main__":
    pytest.main()