import subprocess
import sys
import inquirer


def show_branch() -> None:
    try:
        print("# Cuurent branch ---------------------------------\n")
        subprocess.run(["git", "branch"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error creating branch: {e}")
        sys.exit(1)


def create_branch(branch_name: str) -> None:
    try:
        subprocess.run(["git", "branch", branch_name], check=True)
        print(f"Branch '{branch_name}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating branch: {e}")
        sys.exit(1)


def switch_branch(branch_name: str) -> None:
    try:
        subprocess.run(["git", "checkout", branch_name], check=True)
        print(f"Switched to branch '{branch_name}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error switching branch: {e}")
        sys.exit(1)


def get_action() -> str:
    questions = [
        inquirer.List(
            "action",
            message="Select an action",
            choices=[
                ("1. Create a new branch", "create"),
                ("2. Switch to an existing branch", "switch"),
                ("9. Next", "next"),
            ],
        ),
    ]
    answers = inquirer.prompt(questions)
    return answers["action"]


def get_branch_name() -> str:
    questions = [inquirer.Text("branch_name", message="Enter the branch name")]
    answers = inquirer.prompt(questions)
    return answers["branch_name"]


def main() -> None:
    while True:
        show_branch()
        action = get_action()

        if action in ["create", "switch"]:
            branch_name = get_branch_name()

            if action == "create":
                create_branch(branch_name)
                switch_branch(branch_name)
            elif action == "switch":
                switch_branch(branch_name)

            break
        elif action in ["next"]:
            break
        else:
            print("Invalid action. Please try again.")


if __name__ == "__main__":
    main()
