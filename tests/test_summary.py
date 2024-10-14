import unittest
from unittest.mock import patch, Mock
from summary import summarize_text
import requests

class TestSummarizeText(unittest.TestCase):

    @patch('summary.requests.post')
    @patch('summary.load_dotenv') 
    def test_summarize_text_success(self, mock_load_dotenv, mock_requests_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'This is a summary of the story.'
                    }
                }
            ]
        }
        mock_requests_post.return_value = mock_response
        
        text = "Once upon a time, there was a story."
        summary = summarize_text(text)
        self.assertEqual(summary, 'This is a summary of the story.')
        mock_requests_post.assert_called_once()  

    @patch('summary.requests.post')
    @patch('summary.load_dotenv')
    def test_summarize_text_no_choices(self, mock_load_dotenv, mock_requests_post):

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': []
        }
        mock_requests_post.return_value = mock_response
        
        text = "Once upon a time, there was a story."
        summary = summarize_text(text)
        self.assertEqual(summary, 'No choices found in the response.')
        mock_requests_post.assert_called_once()  

    @patch('summary.requests.post')
    @patch('summary.load_dotenv')  
    def test_summarize_text_request_failure(self, mock_load_dotenv, mock_requests_post):
        mock_requests_post.side_effect = requests.RequestException("Request failed")
        
        text = "Once upon a time, there was a story."
        summary = summarize_text(text)
        self.assertEqual(summary, "Request failed with error: Request failed")
        mock_requests_post.assert_called_once()  

if __name__ == '__main__':
    unittest.main()
