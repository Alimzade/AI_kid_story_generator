import unittest
from unittest.mock import patch, Mock
from generate_story import generate_story

class TestGenerateStory(unittest.TestCase):

    @patch('generate_story.os.getenv')
    @patch('generate_story.requests.post')
    def test_generate_story_success(self, mock_post, mock_getenv):
        mock_getenv.return_value = 'mock_api_key'  
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {'content': 'Once upon a time, Alex went on an adventure...'}
            }]
        }
        mock_post.return_value = mock_response

        data = {
            "protagonistName": "Alex",
            "protagonistGender": "male",
            "storyTheme": "Adventure",
            "ageGroup": "5-7",
            "educationalContent": "Sharing",
            "friendName": "Jordan",
            "friendGender": "female",
            "storyDescription": "a great adventure",
            "storyLength": "short"
        }
        
        result = generate_story(data)
        expected_result = 'Once upon a time, Alex went on an adventure...'
        self.assertEqual(result, expected_result)

    @patch('generate_story.os.getenv')
    @patch('generate_story.requests.post')
    def test_generate_story_failure(self, mock_post, mock_getenv):
        mock_getenv.return_value = 'mock_api_key'
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.side_effect = lambda: {'error': 'Something went wrong'}
        mock_post.return_value = mock_response

        data = {
            "protagonistName": "Alex",
            "protagonistGender": "male",
            "storyTheme": "Adventure",
            "ageGroup": "5-7",
            "educationalContent": "Sharing",
            "friendName": "Jordan",
            "friendGender": "female",
            "storyDescription": "a great adventure",
            "storyLength": "short"
        }

        result = generate_story(data)
        expected_result = 'Request failed with status code 500'
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()