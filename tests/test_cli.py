import unittest
import sys
sys.path.insert(0, './src')
from cli import parse_command, provide_feedback
from unittest.mock import patch

class TestCLI(unittest.TestCase):

    @patch('sys.argv', ['cli.py', 'init'])
    def test_parse_command(self):
        args = parse_command()
        self.assertEqual(args.command, 'init')

    @patch('builtins.print')
    def test_provide_feedback_success(self, mock_print):
        provide_feedback('init', True)
        mock_print.assert_called_with("Command 'init' executed successfully.")

    @patch('builtins.print')
    def test_provide_feedback_failure(self, mock_print):
        provide_feedback('init', False)
        mock_print.assert_called_with("Command 'init' failed. Please try again.")

if __name__ == '__main__':
    unittest.main()
