import os

from agents.ai_base_agent import AIBaseAgent

from utils.load_yaml import load_yaml
from utils.color_print import gprint


class InfraDiagramsDocumentChecker(AIBaseAgent):
    def __init__(
        self,
        diagrams_document: str,
    ):
        super().__init__("InfraDiagramsDocumentChecker")
        self.diagrams_document = diagrams_document

        script_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.join(
            script_dir,
            "prompts",
            "diagrams_document_checker.yaml",
        )
        self.prompt = load_yaml(yaml_path).get("prompt")

    def exec(self) -> str:

        if self.diagrams_document is None:
            raise ValueError("Diagram document is required.")
        return self.check_document()

    def check_document(self) -> str:
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

            check_list: str = self.run(
                messages,
                input_data={
                    "diagrams_document": self.diagrams_document,
                },
            )
            return check_list

        except Exception as e:
            print(f"要件文書の生成中にエラーが発生しました: {str(e)}")
            return "要件文書の生成中にエラーが発生しました。"


if __name__ == "__main__":
    agent = InfraDiagramsDocumentChecker("diagrams_document")
    agent.main()
