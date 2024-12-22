import os

from agents.base_agent import BaseAgent
from utils.git import get_git_root
from utils.readme import append_to_readme, clear_readme


class ResetReadmeAgent(BaseAgent):
    def __init__(self):
        super().__init__("ResetReadmeAgent")

    def main(self):
        project_name = self.get_project_name()
        self.reset_readme(project_name)
        print(
            f"README.md has been reset "
            f"and the project title has been added: {project_name}"
        )

    def get_project_name(self):
        git_root = get_git_root()
        return os.path.basename(git_root)

    def reset_readme(self, project_name):
        clear_readme()
        append_to_readme(f"# {project_name}", header="")


if __name__ == "__main__":
    agent = ResetReadmeAgent()
    agent.main()
