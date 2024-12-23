from typing import List

from agents.ai_base_agent import AIBaseAgent
from agents.multi_agent.persona_generator import PersonaGenerator
from agents.multi_agent.interview_conductor import (
    Interview,
    InterviewConductor,
)
from utils.color_print import gprint


class RequirementsDocumentGenerator(AIBaseAgent):
    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        user_request: str = None,
        interviews: List[Interview] = None,
    ):
        super().__init__("RequirementsDocumentGenerator", model_name)
        self.user_request = user_request
        self.interviews = interviews or []

    def exec(self) -> str:
        if self.user_request is None:
            raise ValueError("User request is required.")

        try:
            messages = [
                (
                    "system",
                    "あなたは収集した情報に基づいて要件文書を作成する専門家です。",
                ),
                (
                    "human",
                    "以下のユーザーリクエストと複数のペルソナからのインタビュー結果に基づいて、要件文書を作成してください。\n\n"
                    "ユーザーリクエスト: {user_request}\n\n"
                    "インタビュー結果:\n{interview_results}\n"
                    "要件文書には以下のセクションを含めてください:\n"
                    "1. プロジェクト概要\n"
                    "2. 主要機能\n"
                    "3. 非機能要件\n"
                    "4. 制約条件\n"
                    "5. ターゲットユーザー\n"
                    "6. 優先順位\n"
                    "7. リスクと軽減策\n\n"
                    "出力は必ず日本語でお願いします。\n\n要件文書:",
                ),
            ]

            requirements_doc: str = self.run(
                messages,
                input_data={
                    "user_request": self.user_request,
                    "interview_results": self._format_interviews(
                        self.interviews,
                    ),
                },
            )
            self._print_requirements(requirements_doc)
            return requirements_doc
        except Exception as e:
            print(f"要件文書の生成中にエラーが発生しました: {str(e)}")
            return "要件文書の生成中にエラーが発生しました。"

    def _format_interviews(self, interviews: List[Interview]) -> str:
        return "\n".join(
            f"ペルソナ: {i.persona.name} - {i.persona.background}\n"
            f"質問: {i.question}\n回答: {i.answer}\n"
            for i in interviews
        )

    def _print_requirements(self, requirements_doc: str) -> None:
        gprint("生成された要件文書:")
        gprint(requirements_doc)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="ユーザー要求に基づいてインタビューを実施します"
    )
    parser.add_argument(
        "--task", type=str, help="作成したいアプリケーションについて記載してください"
    )

    args = parser.parse_args()
    request = args.task or "フィードバックをくれる人"

    persona_generator = PersonaGenerator(user_request=request)
    result_of_persona_generator = persona_generator.main()

    interviewer = InterviewConductor(
        user_request=request,
        personas=result_of_persona_generator.personas,
    )
    interview_result = interviewer.main()

    evaluator = RequirementsDocumentGenerator(
        user_request=request,
        interviews=interview_result.interviews,
    )
    evaluator.main()
