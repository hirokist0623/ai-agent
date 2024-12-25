import os

# from typing import List

from agents.ai_base_agent import AIBaseAgent

from utils.readme import append_to_readme
from utils.load_yaml import load_file, load_yaml


class InfraRequirementsDocumentGenerator(AIBaseAgent):
    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        user_request: str = None,
    ):
        super().__init__("RequirementsDocumentGenerator", model_name)
        self.user_request = user_request

        script_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.join(
            script_dir,
            "prompts",
            "requirement_document.yaml",
        )
        self.prompt = load_yaml(yaml_path).get("prompt")
        file_path = os.path.join(
            script_dir,
            "prompts",
            "requirement_document.md",
        )
        self.document_template = load_file(file_path)

    def exec(self) -> str:

        if self.user_request is None:
            raise ValueError("User request is required.")
        requirements_doc = self.create_document()
        append_to_readme(
            requirements_doc, header="# インフラ要件定義書", file_path="doc/infra/"
        )

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
                    "user_request": self.user_request,
                    "output_format": self.document_template,
                },
            )
            return requirements_doc

        except Exception as e:
            print(f"要件文書の生成中にエラーが発生しました: {str(e)}")
            return "要件文書の生成中にエラーが発生しました。"


if __name__ == "__main__":

    input_request = (
        "google coloudのインフラを作りたいです。cloud runを使って、"
        "デプロイもgithubにmergeした段階で反映したいです。"
    )
    evaluator = InfraRequirementsDocumentGenerator(user_request=input_request)
    evaluator.main()
