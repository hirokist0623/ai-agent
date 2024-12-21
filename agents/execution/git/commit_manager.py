import subprocess
import sys


def add_changes() -> None:
    try:
        subprocess.run(["git", "add", "-A"], check=True)
        print("All changes have been staged.")
    except subprocess.CalledProcessError as e:
        print(f"Error staging changes: {e}")
        sys.exit(1)


def status() -> None:
    try:
        subprocess.run(["git", "status"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error git status: {e}")
        sys.exit(1)


def create_commit_message() -> str:
    print("Enter your commit message (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        elif lines:
            break
    return "\n".join(lines)


def commit_changes(message: str) -> None:
    try:
        subprocess.run(["git", "commit", "-m", message], check=True)
        print("Changes committed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error committing changes: {e}")
        sys.exit(1)


def main() -> None:
    add_changes()

    status()
    commit_message = create_commit_message()
    print(f"\nCommit message:\n{commit_message}\n")

    confirmation = input(
        "Do you want to commit these changes? (y/n): "
    ).lower()  # nosec
    if confirmation == "y":
        commit_changes(commit_message)
    else:
        print("Commit cancelled.")


if __name__ == "__main__":
    main()
