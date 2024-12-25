import os
import sys

from agents.base_agent import BaseAgent

from utils.load_yaml import load_file


class GithubTemplateManager(BaseAgent):
    def __init__(self):
        super().__init__("GithubTemplateManager")
        self.github_dir = ".github"

        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(
            script_dir,
            "md",
            "pull_request_template.md",
        )
        pr_template = load_file(file_path)
        self.template_files = {
            "pull_request_template.md": pr_template,
        }

    def exec(self) -> None:
        self.log_info("Starting GitHub template setup...")

        self.create_github_directory()
        self.create_templates()

    def create_github_directory(self) -> None:
        try:
            os.makedirs(self.github_dir, exist_ok=True)
        except Exception as e:
            self.log_error(f"Error creating directories: {e}")
            sys.exit(1)

    def create_templates(self) -> None:
        for file_path, template_content in self.template_files.items():
            full_path = os.path.join(self.github_dir, file_path)
            try:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(template_content)
                self.log_info(f"Created template: {file_path}")
            except Exception as e:
                self.log_error(f"Error creating template {file_path}: {e}")


if __name__ == "__main__":
    template_manager = GithubTemplateManager()
    template_manager.exec()
