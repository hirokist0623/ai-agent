import subprocess
import sys

from agents.ai_base_agent import AIBaseAgent


class AICommitManager(AIBaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="AICommitManager",
            model_name="gpt-4o-mini",
        )

    def main(self) -> None:
        print(f"Starting AI-assisted commit process using {self.model_name}")
        if not self.check_for_changes():
            print("No changes to commit. Exiting.")
            sys.exit(0)

        self.add_changes()

        self.status()
        commit_message = self.generate_commit_message()
        print(f"\nCommit message:\n{commit_message}\n")

        confirmation = input(
            "Do you want to commit these changes? (y/n): "
        ).lower()  # nosec
        if confirmation == "y":
            self.commit_changes(commit_message)
        else:
            print("Commit cancelled.")

    def check_for_changes(self) -> None:
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True,
            )
            return bool(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            print(f"Error checking git status: {e}")
            sys.exit(1)

    def add_changes(self) -> None:
        try:
            subprocess.run(["git", "add", "-A"], check=True)
            print("All changes have been staged.")
        except subprocess.CalledProcessError as e:
            print(f"Error staging changes: {e}")
            sys.exit(1)

    def status(self) -> None:
        try:
            subprocess.run(["git", "status"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error git status: {e}")
            sys.exit(1)

    def generate_commit_message(self) -> str:
        print("Enter your commit message (press Enter twice to finish):")
        lines = []
        while True:
            line = input()
            if line:
                lines.append(line)
            elif lines:
                break
        return "\n".join(lines)

    def commit_changes(self, message):
        try:
            subprocess.run(["git", "commit", "-m", message], check=True)
            print("Changes committed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error committing changes: {e}")
            sys.exit(1)


if __name__ == "__main__":
    commit_manager = AICommitManager()
    commit_manager.main()
