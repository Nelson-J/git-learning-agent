import unittest
from click.testing import CliRunner

from src.cli import cli


class TestClickCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_cli_init_command(self):
        result = self.runner.invoke(cli, ['init'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Initialized new repository', result.output)

    def test_cli_help_command(self):
        result = self.runner.invoke(cli, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Show this message and exit', result.output)

    def test_cli_invalid_command(self):
        result = self.runner.invoke(cli, ['invalid'])
        self.assertEqual(result.exit_code, 2)
        self.assertIn('Error: No such command', result.output)


if __name__ == "__main__":
    unittest.main()
