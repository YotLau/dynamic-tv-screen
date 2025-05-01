import os
import unittest
from unittest.mock import patch, mock_open
from config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        # Clear any existing environment variables before each test
        for var in Config.REQUIRED_VARS:
            if var in os.environ:
                del os.environ[var]

    def test_validate_env_missing_vars(self):
        # Test when environment variables are missing
        with self.assertRaises(ValueError) as context:
            Config.validate_env()
        self.assertTrue('Missing required environment variables' in str(context.exception))

    def test_validate_env_all_vars_present(self):
        # Test when all required environment variables are present
        test_values = {
            'IDEOGRAM_API_KEY': 'test_key',
            'IDEOGRAM_STYLE_TYPE': 'test_style',
            'IDEOGRAM_ASPECT_RATIO': '1:1',
            'NEGATIVE_PROMPT': 'test_negative',
            'IMAGES_FOLDER': 'test_folder'
        }
        
        with patch.dict(os.environ, test_values):
            try:
                Config.validate_env()
            except ValueError:
                self.fail('validate_env() raised ValueError unexpectedly')

    def test_get_env(self):
        # Test getting environment variable
        test_key = 'TEST_VAR'
        test_value = 'test_value'
        
        with patch.dict(os.environ, {test_key: test_value}):
            result = Config.get_env(test_key)
            self.assertEqual(result, test_value)

    def test_get_env_nonexistent(self):
        # Test getting non-existent environment variable
        result = Config.get_env('NONEXISTENT_VAR')
        self.assertIsNone(result)

    def test_set_env_new_variable(self):
        # Test setting a new environment variable
        test_key = 'TEST_VAR'
        test_value = 'test_value'
        mock_env_content = ''
        
        with patch('builtins.open', mock_open(read_data=mock_env_content)) as mock_file:
            Config.set_env(test_key, test_value)
            
            # Verify environment variable was set
            self.assertEqual(os.environ[test_key], test_value)
            
            # Verify .env file was written to
            mock_file().writelines.assert_called_once()

    def test_set_env_update_existing(self):
        # Test updating an existing environment variable
        test_key = 'TEST_VAR'
        initial_value = 'initial_value'
        new_value = 'new_value'
        mock_env_content = f'{test_key}={initial_value}\n'
        
        with patch('builtins.open', mock_open(read_data=mock_env_content)) as mock_file:
            Config.set_env(test_key, new_value)
            
            # Verify environment variable was updated
            self.assertEqual(os.environ[test_key], new_value)
            
            # Verify .env file was written to
            mock_file().writelines.assert_called_once()

    def test_set_env_file_error(self):
        # Test handling of file write error
        test_key = 'TEST_VAR'
        test_value = 'test_value'
        
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = IOError('Test error')
            
            # Should not raise exception but print warning
            try:
                Config.set_env(test_key, test_value)
            except Exception:
                self.fail('set_env() should handle file errors gracefully')
            
            # Verify environment variable was still set
            self.assertEqual(os.environ[test_key], test_value)

if __name__ == '__main__':
    unittest.main()