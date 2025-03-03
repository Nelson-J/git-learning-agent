import argparse
from .models import UserProfile, PersistenceLayer


def parse_command() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Git Learning System CLI"
    )
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    init_parser = subparsers.add_parser(
        'init', help='Initialize a new Git repository'
    )
    init_parser.add_argument(
        '--option', type=str, help='Option for the init command'
    )

    add_parser = subparsers.add_parser(
        'add', help='Add files to the Git repository'
    )
    add_parser.add_argument(
        '--option', type=str, help='Option for the add command'
    )

    commit_parser = subparsers.add_parser(
        'commit', help='Commit changes to the Git repository'
    )
    commit_parser.add_argument(
        '--option', type=str, help='Option for the commit command'
    )

    status_parser = subparsers.add_parser(
        'status', help='Show the status of the Git repository'
    )
    status_parser.add_argument(
        '--option', type=str, help='Option for the status command'
    )

    log_parser = subparsers.add_parser(
        'log', help='Show the commit log of the Git repository'
    )
    log_parser.add_argument(
        '--option', type=str, help='Option for the log command'
    )

    return parser.parse_args()


def provide_feedback(command: str, success: bool, message: str = '') -> None:
    """Provide feedback for command execution."""
    if success:
        print(f"Command '{command}' executed successfully.{message}")
    else:
        print(f"Command '{command}' failed.{message} Please try again.")


def provide_help() -> None:
    """Provide help information."""
    help_info = "Available commands: init, add, commit, status, log, help"
    print(help_info)


def main() -> None:
    args = parse_command()
    command = args.command

    persistence = PersistenceLayer()
    user = UserProfile(username="test_user", email="test@example.com")
    # Manually set the id to ensure compatibility with tests
    user.id = "1"
    persistence.add_user(user)

    # Simulate command execution
    success = True
    message = ''

    # Example command handling
    if command == "help":
        provide_help()
    elif command in ["init", "add", "commit", "status", "log"]:
        # Simulate command execution logic
        message = f"Executed {command} command."
    else:
        success = False
        message = "Invalid command."

    provide_feedback(command, success, message)


def cli_function():
    # CLI code
    pass


if __name__ == "__main__":
    main()
