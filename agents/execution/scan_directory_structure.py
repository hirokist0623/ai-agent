import os

from typing import Any, Dict

import yaml

from agents.base_agent import BaseAgent
from utils.git import get_git_root


class ScanDirectoryStructureAgent(BaseAgent):
    def __init__(self):
        super().__init__("ScanDirectoryStructureAgent")

    def main(self) -> None:
        print("Scanning directory structure...")
        root_dir = get_git_root()
        structure = self.scan_directory(root_dir)
        self.save_to_yaml(structure)

    def scan_directory(self, directory: str) -> Dict[str, Any]:
        """Recursively scan the directory and return its structure."""
        structure = {}
        for item in os.listdir(directory):
            if item.startswith(".") and item != ".ai_base":
                continue
            path = os.path.join(directory, item)
            if os.path.isdir(path):
                structure[item] = self.scan_directory(path)
            else:
                structure[item] = None
        return structure

    def save_to_yaml(self, structure: Dict[str, Any]) -> None:
        """Save the directory structure to a YAML file."""
        output_dir = os.path.join(get_git_root(), ".ai_base")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "directory_structure.yaml")
        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(structure, f, default_flow_style=False)


if __name__ == "__main__":
    agent = ScanDirectoryStructureAgent()
    agent.main()
