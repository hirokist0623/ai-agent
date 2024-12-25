import os

from agents.ai_base_agent import AIBaseAgent

from utils.readme import append_to_readme
from utils.git import get_git_root
from utils.load_yaml import load_file, load_yaml


class InfraDiagramsDocumentGenerator(AIBaseAgent):
    def __init__(
        self,
    ):
        super().__init__("RequirementsDocumentGenerator")
        git_root = get_git_root()
        file_path = os.path.join(
            git_root,
            "docs",
            "infra",
            "README.md",
        )
        self.requirements_document = load_file(file_path)

        script_dir = os.path.dirname(os.path.abspath(__file__))

        yaml_path = os.path.join(
            script_dir,
            "prompts",
            "diagrams_document.yaml",
        )
        self.prompt = load_yaml(yaml_path).get("prompt")

        file_path = os.path.join(
            script_dir,
            "md",
            "diagrams_document.md",
        )
        self.document_template = load_file(file_path)

    def exec(self) -> str:

        if self.requirements_document is None:
            raise ValueError("User request is required.")
        requirements_doc = self.create_document()
        append_to_readme(requirements_doc, header="## インフラ構成図")

    def create_document(self) -> str:
        try:
            messages = [
                (
                    "system",
                    self.prompt.get("system"),
                ),
                (
                    "human",
                    self.prompt.get("template"),
                ),
            ]

            requirements_doc: str = self.run(
                messages,
                input_data={
                    "requirements_document": self.requirements_document,
                    "output_format": self.document_template,
                },
            )
            return requirements_doc

        except Exception as e:
            print(f"要件文書の生成中にエラーが発生しました: {str(e)}")
            return "要件文書の生成中にエラーが発生しました。"


if __name__ == "__main__":
    evaluator = InfraDiagramsDocumentGenerator()
    evaluator.main()
