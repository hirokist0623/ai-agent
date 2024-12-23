import subprocess
import sys
import os

from langchain_core.messages import SystemMessage, HumanMessage

from agents.ai_base_agent import AIBaseAgent
from utils.load_yaml import load_yaml
from utils.color_print import gprint, iinput


class AICommitManager(AIBaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="AICommitManager",
            model_name="gpt-4o-mini",
        )

        script_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.join(script_dir, "prompts", "commit_message.yaml")
        self.prompts = load_yaml(yaml_path)

    def exec(self) -> None:
        print(f"Starting AI-assisted commit process using {self.model_name}")
        if not self.check_for_changes():
            print("No changes to commit. Exiting.")
            sys.exit(0)

        self.add_changes()

        self.status()
        commit_message = self.generate_commit_message()
        print(f"\nCommit message:\n")
        gprint(f"{commit_message}\n")

        confirmation = iinput(
            "Do you want to commit these changes? (y/n): "
        ).lower()  # nosec
        if confirmation == "y":
            self.commit_changes(commit_message)
        else:
            print("Commit cancelled.")

    def check_for_changes(self) -> bool:
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
            subprocess.run(["git", "add", "-p"], check=True)
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

    def get_diff_summary(self) -> tuple[str, str]:
        """変更内容の要約を取得します"""
        try:
            # ステージングされた変更の統計を取得
            result = subprocess.run(
                ["git", "diff", "--cached", "--stat"],
                capture_output=True,
                text=True,
                check=True,
            )
            stats = result.stdout.strip()

            # 詳細な差分を取得
            result = subprocess.run(
                ["git", "diff", "--cached"],
                capture_output=True,
                text=True,
                check=True,
            )
            diff = result.stdout.strip()

            return stats, diff
        except subprocess.CalledProcessError as e:
            print(f"Error getting diff: {e}")
            sys.exit(1)

    def generate_commit_message(self) -> str:
        """AIを使用してコミットメッセージを生成します"""
        diff_stats, diff_content = self.get_diff_summary()

        # プロンプトテンプレートを準備
        system_prompt = self.prompts["commit_message"]["system"]
        user_prompt = self.prompts["commit_message"]["user"].format(
            diff_stats=diff_stats, diff_content=diff_content
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        return self.run(messages)

    def commit_changes(self, message: str) -> None:
        try:
            subprocess.run(["git", "commit", "-m", message], check=True)
            print("変更が正常にコミットされました。")
        except subprocess.CalledProcessError as e:
            print(f"Error committing changes: {e}")
            sys.exit(1)


if __name__ == "__main__":
    commit_manager = AICommitManager()
    commit_manager.main()
