import os
import sys
from git import Repo, GitCommandError
from agents.base_agent import BaseAgent


class GitCleanupAgent(BaseAgent):
    def __init__(self):
        super().__init__("GitCleanupAgent")
        self.repo = self.get_repo()
        self.main_branch = self.get_main_branch()

    def exec(self):
        self.switch_to_main()
        self.pull_latest_changes()
        self.delete_merged_branches()

    def get_repo(self):
        try:
            return Repo(os.getcwd())
        except GitCommandError as e:
            print(f"Failed to initialize Git repository: {e}")
            sys.exit(1)

    def get_main_branch(self):
        try:
            return (
                self.repo.heads["main"]
                if "main" in self.repo.heads
                else self.repo.heads["master"]
            )
        except IndexError:
            print("Neither 'main' nor 'master' branch found.")
            sys.exit(1)

    def switch_to_main(self):
        try:
            self.main_branch.checkout()
        except GitCommandError as e:
            print(f"Failed to switch to {self.main_branch.name} branch: {e}")
            sys.exit(1)

    def pull_latest_changes(self):
        try:
            self.repo.remotes.origin.pull()
            name = self.main_branch.name
            print(f"Successfully pulled latest changes from {name}")
        except GitCommandError as e:
            print(f"Failed to pull latest changes: {e}")
            sys.exit(1)

    def delete_merged_branches(self):
        try:
            merged_branches = [
                branch
                for branch in self.repo.heads
                if branch != self.main_branch
                and self.repo.is_ancestor(
                    branch.commit,
                    self.main_branch.commit,
                )
            ]
            for branch in merged_branches:
                prompt = f"Delete branch '{branch.name}'? (y/n): "
                if input(prompt).lower() == "y":
                    self.repo.delete_head(branch, force=True)
                    print(f"Deleted branch: {branch.name}")
                else:
                    print(f"Skipped deleting branch: {branch.name}")
        except GitCommandError as e:
            print(f"Failed to delete merged branches: {e}")


if __name__ == "__main__":
    agent = GitCleanupAgent()
    agent.main()
