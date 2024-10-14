import unittest
from unittest.mock import patch
from auth import get_password_hash, verify_password

class TestAuth(unittest.TestCase):
    
    @patch('auth.pwd_context.hash')
    @patch('auth.pwd_context.verify')
    def test_hash_and_verify(self, mock_verify, mock_hash):
        # Mock the hash and verify methods
        mock_hash.return_value = 'fakehashedpassword'
        mock_verify.return_value = True
        
        password = "testpassword"
        
        # Test get_password_hash
        hashed = get_password_hash(password)
        self.assertEqual(hashed, 'fakehashedpassword')
        mock_hash.assert_called_once_with(password)
        
        # Test verify_password
        result = verify_password(password, hashed)
        self.assertTrue(result)
        mock_verify.assert_called_once_with(password, hashed)

if __name__ == '__main__':
    unittest.main()