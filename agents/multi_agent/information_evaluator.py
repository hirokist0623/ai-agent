from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from agents.ai_base_agent import AIBaseAgent

from agents.multi_agent.persona_generator import PersonaGenerator
from agents.multi_agent.interview_conductor import (
    Interview,
    InterviewConductor,
)

from utils.color_print import gprint


class EvaluationResult(BaseModel):
    reason: str = Field(..., description="判断の理由")
    is_sufficient: bool = Field(..., description="情報が十分かどうか")


class InformationEvaluator(AIBaseAgent):
    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        user_request: str = None,
        interviews: List[Interview] = None,
    ):
        super().__init__("InformationEvaluator", model_name, EvaluationResult)
        self.user_request = user_request
        self.interviews = interviews or []

    def exec(self) -> EvaluationResult:
        if self.user_request is None:
            raise ValueError("User request is required.")

        try:
            messages = [
                (
                    "system",
                    "あなたは包括的な要件文書を作成するための情報の十分性を評価する専門家です。",
                ),
                (
                    "human",
                    "以下のユーザーリクエストとインタビュー結果に基づいて、"
                    "包括的な要件文書を作成するのに十分な情報が集まったかどうかを判断してください。\n\n"
                    "ユーザーリクエスト: {user_request}\n\n"
                    "インタビュー結果:\n{interview_results}",
                ),
            ]

            result: EvaluationResult = self.run(
                messages,
                input_data={
                    "user_request": self.user_request,
                    "interview_results": self._format_interviews(),
                },
            )
            self._print_evaluation(result)
            return result
        except Exception as e:
            print(f"情報の評価中にエラーが発生しました: {str(e)}")
            return EvaluationResult(
                reason="評価中にエラーが発生しました", is_sufficient=False
            )

    def _format_interviews(self) -> str:
        return "\n".join(
            f"ペルソナ: {i.persona.name} - {i.persona.background}\n"
            f"質問: {i.question}\n回答: {i.answer}\n"
            for i in self.interviews
        )

    def _print_evaluation(self, result: EvaluationResult) -> None:
        print("評価結果:")
        gprint(f"情報の十分性: {'十分' if result.is_sufficient else '不十分'}")
        gprint(f"理由: {result.reason}")


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

    evaluator = InformationEvaluator(
        user_request=request,
        interviews=interview_result.interviews,
    )
    evaluator.main()
