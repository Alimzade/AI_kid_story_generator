import unittest
from unittest.mock import patch, Mock
from gender_comparison import generate_story, compare_stories, protagonists

class TestGenderComparison(unittest.TestCase):

    @patch('gender_comparison.requests.post')
    def test_generate_story_success(self, mock_requests_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'This is a story with a male protagonist.'
                    }
                }
            ]
        }
        mock_requests_post.return_value = mock_response

        story = generate_story(protagonists[0]['name'], protagonists[0]['gender'], protagonists[0]['theme'])
        
        self.assertEqual(story, 'This is a story with a male protagonist.')
        mock_requests_post.assert_called_once()  

    @patch('gender_comparison.requests.post')
    def test_generate_story_failure(self, mock_requests_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_requests_post.return_value = mock_response
        
        story = generate_story(protagonists[0]['name'], protagonists[0]['gender'], protagonists[0]['theme'])
        
        self.assertIsNone(story)
        mock_requests_post.assert_called_once()  

    @patch('gender_comparison.requests.post')
    @patch('builtins.print')
    def test_compare_stories_success(self, mock_print, mock_requests_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'The stories are similar with no significant gender stereotypes.'
                    }
                }
            ]
        }
        mock_requests_post.return_value = mock_response

        story_male = 'This is a story with a male protagonist.'
        story_female = 'This is a story with a female protagonist.'
        compare_stories(story_male, story_female)
        
        mock_print.assert_called_once_with('Comparison Result:\n', 'The stories are similar with no significant gender stereotypes.')
        mock_requests_post.assert_called_once()  

    @patch('gender_comparison.requests.post')
    @patch('builtins.print')
    def test_compare_stories_failure(self, mock_print, mock_requests_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_requests_post.return_value = mock_response

        story_male = 'This is a story with a male protagonist.'
        story_female = 'This is a story with a female protagonist.'
        compare_stories(story_male, story_female)
        
        mock_print.assert_called_once_with('Request failed with status code 500')
        mock_requests_post.assert_called_once()  

if __name__ == '__main__':
    unittest.main()
