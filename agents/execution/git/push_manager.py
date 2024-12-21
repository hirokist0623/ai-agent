import subprocess
import sys


def get_current_branch() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting current branch: {e}")
        sys.exit(1)


def push_changes(branch: str) -> None:
    try:
        subprocess.run(["git", "push", "origin", branch], check=True)
        print(f"Changes pushed to origin/{branch} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error pushing changes: {e}")
        sys.exit(1)


def main() -> None:
    current_branch = get_current_branch()
    print(f"Current branch: {current_branch}")

    confirmation = input(
        f"Do you want to push changes to origin/{current_branch}? (y/n): "
    ).lower()
    if confirmation == "y":
        push_changes(current_branch)
    else:
        print("Push cancelled.")


if __name__ == "__main__":
    main()
