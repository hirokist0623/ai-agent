import os
from typing import Dict, Any

from agents.base_agent import BaseAgent
from utils.load_yaml import load_yaml
from utils.git import get_git_root
from utils.readme import append_to_readme

# Define files and folders to exclude
EXCLUDE_FOLDERS = [
    "__pycache__",
]

EXCLUDE_FILES = [
    "__init__.py",
    "*.pyc",
]


class CreateStructureAgent(BaseAgent):
    def __init__(self):
        super().__init__("CreateStructureAgent")

    def main(self):
        project_name = self.get_project_name()
        structure = self.load_scanned_structure()
        filtered_structure = self.filter_structure(structure)
        formatted_structure = self.format_structure(
            filtered_structure,
            project_name,
        )
        self.print_structure(formatted_structure)

    def get_project_name(self):
        git_root = get_git_root()
        return os.path.basename(git_root)

    def load_scanned_structure(self) -> Dict[str, Any]:
        git_root = get_git_root()
        yaml_path = os.path.join(
            git_root,
            ".ai_base",
            "directory_structure.yaml",
        )
        return load_yaml(yaml_path)

    def filter_structure(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        filtered = {}
        for name, content in structure.items():
            if self.should_include(
                name, is_directory=isinstance(content, dict)
            ):  # noqa
                if isinstance(content, dict):
                    filtered_content = self.filter_structure(content)
                    if filtered_content:
                        filtered[name] = filtered_content
                else:
                    filtered[name] = content
        return filtered

    def should_include(self, name: str, is_directory: bool) -> bool:
        if is_directory:
            return name not in EXCLUDE_FOLDERS
        else:
            return not any(
                self.match_pattern(name, pattern) for pattern in EXCLUDE_FILES
            )

    def match_pattern(self, name: str, pattern: str) -> bool:
        if pattern.startswith("*"):
            return name.endswith(pattern[1:])
        return name == pattern

    def format_structure(
        self, structure: Dict[str, Any], project_name: str, prefix: str = ""
    ) -> str:
        lines = []
        if prefix == "":
            lines.append(f"{project_name}/")

        items = sorted(structure.items())
        for i, (name, subtree) in enumerate(items):
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            lines.append(f"{prefix}{current_prefix}{name}")

            if isinstance(subtree, dict):
                if is_last:
                    new_prefix = prefix + "    "
                else:
                    new_prefix = prefix + "│   "
                lines.append(
                    self.format_structure(
                        subtree,
                        project_name,
                        new_prefix,
                    )
                )

        return "\n".join(lines)

    def print_structure(self, structure):
        append_to_readme(structure, "## Directory Structure")


if __name__ == "__main__":
    agent = CreateStructureAgent()
    agent.main()
