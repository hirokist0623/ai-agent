import subprocess
import sys
import inquirer

from agents.base_agent import BaseAgent


class BranchManager(BaseAgent):
    def __init__(self):
        super().__init__("BranchManager")

    def exec(self) -> None:
        while True:
            self.show_branch()
            action = self.get_action()

            if action in ["create", "switch"]:
                branch_name = self.get_branch_name()

                if action == "create":
                    self.create_branch(branch_name)
                    self.switch_branch(branch_name)
                elif action == "switch":
                    self.switch_branch(branch_name)

                break
            elif action in ["next"]:
                break
            else:
                print("Invalid action. Please try again.")

    def show_branch(self) -> None:
        try:
            subprocess.run(["git", "branch"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error displaying branches: {e}")
            sys.exit(1)

    def create_branch(self, branch_name: str) -> None:
        try:
            subprocess.run(["git", "branch", branch_name], check=True)
            print(f"Branch '{branch_name}' created successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating branch: {e}")
            sys.exit(1)

    def switch_branch(self, branch_name: str) -> None:
        try:
            subprocess.run(["git", "checkout", branch_name], check=True)
            print(f"Switched to branch '{branch_name}'.")
        except subprocess.CalledProcessError as e:
            print(f"Error switching branch: {e}")
            sys.exit(1)

    def get_action(self) -> str:
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

    def get_branch_name(self) -> str:
        questions = [
            inquirer.Text(
                "branch_name",
                message="Enter the branch name",
            )
        ]
        answers = inquirer.prompt(questions)
        return answers["branch_name"]


if __name__ == "__main__":
    branch_manager = BranchManager()
    branch_manager.main()
