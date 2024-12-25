import os
from agents.ai_base_agent import AIBaseAgent
from utils.load_yaml import load_file, load_yaml
from utils.color_print import gprint, iinput


class InfraHearingAgent(AIBaseAgent):
    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
    ):
        super().__init__("InfraHearingAgent", model_name)
        self.conversation = []

        script_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.join(
            script_dir,
            "prompts",
            "hearing_agent.yaml",
        )
        self.prompt = load_yaml(yaml_path).get("prompt")
        file_path = os.path.join(
            script_dir,
            "prompts",
            "requirement_document.md",
        )
        self.document_template = load_file(file_path)

    def exec(self) -> str:
        try:
            final_request = self.conduct_hearing()
            return final_request
        except Exception as e:
            print(f"ヒアリング中にエラーが発生しました: {str(e)}")
            return "ヒアリング中にエラーが発生しました。"

    def conduct_hearing(self) -> str:
        while True:
            question = self._generate_next_question()
            print("\nエージェント: " + question)

            user_response = input("あなた: ")
            self.conversation.append(f"Q: {question}\nA: {user_response}")

            if self._check_satisfaction():
                break

        return self._generate_final_request()

    def _generate_next_question(self) -> str:
        messages = [
            (
                "system",
                self.prompt.get("system"),
            ),
            (
                "human",
                self.prompt.get("question_template"),
            ),
        ]

        question = self.run(
            messages,
            input_data={
                "output_format": self.document_template,
                "conversation_history": "\n\n".join(self.conversation),
            },
        )
        return question

    def _check_satisfaction(self) -> bool:
        messages = [
            (
                "system",
                self.prompt.get("system"),
            ),
            (
                "human",
                self.prompt.get("satisfied_template"),
            ),
        ]

        satisfaction_message = self.run(
            messages,
            input_data={
                "output_format": self.document_template,
                "conversation_history": "\n\n".join(self.conversation),
            },
        )
        gprint(satisfaction_message)
        response = iinput("\nヒアリングを終了しますか？ [y/n]: ")
        return response.lower() == "yes" or response.lower() == "y"

    def _generate_final_request(self) -> str:
        messages = [
            (
                "system",
                self.prompt.get("system"),
            ),
            (
                "human",
                self.prompt.get("summary_template"),
            ),
        ]

        final_request = self.run(
            messages,
            input_data={"conversation_history": "\n\n".join(self.conversation)},
        )

        print("\n最終的なリクエスト文章:")
        gprint(final_request)
        return final_request


if __name__ == "__main__":
    agent = InfraHearingAgent()
    agent.main()
