import unittest
from unittest.mock import patch, MagicMock
from evaluation import (
    evaluate_options,
    evaluate_length,
    evaluate_readability,
    check_for_harmful_content
)

class TestEvaluation(unittest.TestCase):
    
    def test_evaluate_options(self):
        story = "Alex went on an adventure with Jordan. It taught him about Sharing."
        data = {
            "protagonistName": "Alex",
            "storyTheme": "Adventure",
            "friendName": "Jordan",
            "educationalContent": "Sharing"
        }
        expected_result = {
            "options_evaluations": (
                True,
                {
                    "protagonist_name": '✔️',
                    "story_theme": '✔️',
                    "friend_name": '✔️',
                    "educational_content": '✔️'
                }
            )
        }
        result = evaluate_options(story, data)
        self.assertEqual(result, expected_result)

    def test_evaluate_length_short(self):
        story = "This is a short story."
        expected_length = "short"
        expected_result = {"length_evaluation": ('✔️', len(story.split()))}
        result = evaluate_length(story, expected_length)
        self.assertEqual(result, expected_result)

    def test_evaluate_length_medium(self):
        story = "This is a medium length story." * 50
        expected_length = "medium"
        expected_result = {"length_evaluation": ('✔️', len(story.split()))}
        result = evaluate_length(story, expected_length)
        self.assertEqual(result, expected_result)

    def test_evaluate_length_long(self):
        story = "This is a very long story." * 120
        expected_length = "long"
        expected_result = {"length_evaluation": ('✔️', len(story.split()))}
        result = evaluate_length(story, expected_length)
        self.assertEqual(result, expected_result)
    
    @patch('evaluation.textstat.flesch_reading_ease')
    @patch('evaluation.textstat.flesch_kincaid_grade')
    def test_evaluate_readability(self, mock_flesch_grade, mock_flesch_score):
        story = "This is a test story for readability."
        age_group = "4-6"
        
        mock_flesch_score.return_value = 85
        mock_flesch_grade.return_value = 5
        
        expected_result = {
            "readability_evaluation": {
                "flesch_score": 85,
                "flesch_grade": 5,
                "appropriate_for_age_group": True,
                "score_color": "green"
            }
        }
        
        result = evaluate_readability(story, age_group)
        self.assertEqual(result, expected_result)
    
    @patch('evaluation.requests.post')
    @patch('evaluation.os.getenv')
    def test_check_for_harmful_content(self, mock_getenv, mock_post):
        mock_getenv.return_value = "fake_api_url"
        mock_post.return_value = MagicMock(status_code=200)
        mock_post.return_value.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Safe: Yes\nHarmful Content Found: No\nDetails: None"
                    }
                }
            ]
        }
        
        story = "This is a test story."
        age_group = "6-9"
        expected_result = {
            "evaluation": "No harmful content",
            "content": "Safe: Yes\nHarmful Content Found: No\nDetails: None"
        }
        
        result = check_for_harmful_content(story, age_group)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
