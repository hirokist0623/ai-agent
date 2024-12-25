import os

# from typing import List

from agents.ai_base_agent import AIBaseAgent

from utils.load_yaml import load_file, load_yaml
from utils.color_print import gprint


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
        self.create_document()

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
            self._print_requirements(requirements_doc)
            return requirements_doc

        except Exception as e:
            print(f"要件文書の生成中にエラーが発生しました: {str(e)}")
            return "要件文書の生成中にエラーが発生しました。"

    def _print_requirements(self, requirements_doc: str) -> None:
        print("生成された要件文書:")
        gprint(requirements_doc)


if __name__ == "__main__":

    input_request = (
        "google coloudのインフラを作りたいです。cloud runを使って、"
        "デプロイもgithubにmergeした段階で反映したいです。"
    )
    evaluator = InfraRequirementsDocumentGenerator(user_request=input_request)
    evaluator.main()
