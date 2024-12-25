import os

from agents.ai_base_agent import AIBaseAgent

from agents.planning.infra.diagrams_document_cheker import (
    InfraDiagramsDocumentChecker,
)

from utils.readme import append_to_readme
from utils.git import get_git_root
from utils.load_yaml import load_file, load_yaml
from utils.color_print import gprint


class InfraDiagramsDocumentGenerator(AIBaseAgent):
    def __init__(
        self,
    ):
        super().__init__("RequirementsDocumentGenerator")
        self.check_list: str = ""
        self.previous_diagrams_document: str = ""

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

        # self.previous_diagrams_document = requirements_doc
        # gprint(self.previous_diagrams_document)

        # cheker = InfraDiagramsDocumentChecker(self.previous_diagrams_document)
        # self.check_list = cheker.exec()
        # gprint(self.check_list)

        # requirements_doc = self.modify_document()

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
                    self.prompt.get("create_template"),
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

    def modify_document(self) -> str:
        try:
            messages = [
                (
                    "system",
                    self.prompt.get("system"),
                ),
                (
                    "human",
                    self.prompt.get("modify_template"),
                ),
            ]

            requirements_doc: str = self.run(
                messages,
                input_data={
                    "requirements_document": self.requirements_document,
                    "output_format": self.document_template,
                    "previous_diagrams_document": self.previous_diagrams_document,  # noqa
                    "check_list": self.check_list,
                },
            )
            return requirements_doc

        except Exception as e:
            print(f"要件文書の生成中にエラーが発生しました: {str(e)}")
            return "要件文書の生成中にエラーが発生しました。"


if __name__ == "__main__":
    evaluator = InfraDiagramsDocumentGenerator()
    evaluator.main()
