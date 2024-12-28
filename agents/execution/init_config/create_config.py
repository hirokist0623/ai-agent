import os
from datetime import datetime
from agents.base_agent import BaseAgent


class InitConfigAgent(BaseAgent):
    def __init__(self):
        super().__init__("InitConfig")
        self.root_dir = self.find_git_root()
        self.ai_agents_dir = os.path.join(self.root_dir, ".ai_agents")
        self.config_file = os.path.join(self.ai_agents_dir, "config.yaml")
        self.log_dir = os.path.join(self.ai_agents_dir, "logs")
        self.gitignore_file = os.path.join(self.root_dir, ".gitignore")

    def main(self):
        self.create_directory(self.ai_agents_dir)
        self.create_directory(self.log_dir)
        self.create_config_file()
        self.setup_logging()
        self.update_gitignore()

    def find_git_root(self):
        current_dir = os.getcwd()
        while current_dir != "/":
            if os.path.exists(os.path.join(current_dir, ".git")):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        raise Exception("Not in a git repository")

    def create_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created directory: {path}")
        else:
            print(f"Directory already exists: {path}")

    def create_config_file(self):
        if not os.path.exists(self.config_file):
            config_comment: str = """
# description: AI Agent for automating git operations and PR creation,
# github_url: https://github.com/yourusername/your-repo-name,
"""
            with open(self.config_file, "w", encoding="utf-8") as f:
                f.write(config_comment)
            print(f"Created config file: {self.config_file}")
        else:
            print(f"Config file already exists: {self.config_file}")

    def setup_logging(self):
        log_file = os.path.join(
            self.log_dir, f"{datetime.now().strftime('%Y-%m-%d')}_log.txt"
        )
        if not os.path.exists(log_file):
            open(log_file, "a", encoding="utf-8").close()
            print(f"Created log file: {log_file}")
        else:
            print(f"Log file already exists: {log_file}")

    def update_gitignore(self):
        gitignore_entry = ".ai_agents"

        # Create .gitignore if it doesn't exist
        if not os.path.exists(self.gitignore_file):
            with open(self.gitignore_file, "w", encoding="utf-8") as f:
                f.write(f"{gitignore_entry}\n")
            print(f"Created .gitignore and added {gitignore_entry}")
            return

        # Check if .ai_agents is already in .gitignore
        with open(self.gitignore_file, "r", encoding="utf-8") as f:
            content = f.read()
            if gitignore_entry in content.split("\n"):
                print(f"{gitignore_entry} is already in .gitignore")
                return

        # Append .ai_agents to .gitignore
        with open(self.gitignore_file, "a", encoding="utf-8") as f:
            f.write(f"\n{gitignore_entry}\n")
        print(f"Added {gitignore_entry} to .gitignore")


if __name__ == "__main__":
    agent = InitConfigAgent()
    agent.main()
