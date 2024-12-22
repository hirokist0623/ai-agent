import subprocess
import sys
import inquirer
from agents.base_agent import BaseAgent
from utils.color_print import gprint


class PushManager(BaseAgent):
    def __init__(self):
        super().__init__("PushManager")

    def exec(self) -> None:
        current_branch = self.get_current_branch()
        gprint(f"Current branch: {current_branch}")

        action = self.get_action(current_branch)

        if action == "push":
            self.push_changes(current_branch)
        else:
            print("Push cancelled.")

    def get_current_branch(self) -> str:
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

    def push_changes(self, branch: str) -> None:
        try:
            subprocess.run(["git", "push", "origin", branch], check=True)
            print(f"Changes pushed to origin/{branch} successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error pushing changes: {e}")
            sys.exit(1)

    def get_action(self, current_branch: str) -> str:
        questions = [
            inquirer.List(
                "action",
                message=(
                    f"Do you want to push changes to origin/{current_branch}?"
                ),  # noqa
                choices=[
                    ("Yes, push changes", "push"),
                    ("No, cancel", "cancel"),
                ],
            ),
        ]
        answers = inquirer.prompt(questions)
        return answers["action"]


if __name__ == "__main__":
    push_manager = PushManager()
    push_manager.exec()
