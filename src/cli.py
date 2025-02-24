import argparse
from .models import UserProfile, PersistenceLayer


def parse_command() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Git Learning System CLI")
    parser.add_argument("command", type=str, help="Git command to execute")
    parser.add_argument("--option", type=str, help="Option for the Git command")
    return parser.parse_args()


def provide_feedback(command: str, success: bool) -> None:
    """Provide feedback for command execution."""
    if success:
        print(f"Command '{command}' executed successfully.")
    else:
        print(f"Command '{command}' failed. Please try again.")


def main() -> None:
    args = parse_command()
    command = args.command

    persistence = PersistenceLayer()
    user = UserProfile(user_id="1", username="test_user", email="test@example.com")
    persistence.add_user(user)

    # Simulate command execution
    success = True
    provide_feedback(command, success)

    # Help system foundation
    if command == "help":
        print("Available commands: init, add, commit, status, log, help")


if __name__ == "__main__":
    main()
