from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from agents.ai_base_agent import AIBaseAgent
from agents.multi_agent.interview_conductor import Interview
from utils.color_print import gprint, iprint

class EvaluationResult(BaseModel):
    reason: str = Field(..., description="判断の理由")
    is_sufficient: bool = Field(..., description="情報が十分かどうか")

class InformationEvaluator(AIBaseAgent):
    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        user_request: str = None,
    ):
        super().__init__("InformationEvaluator", model_name, EvaluationResult)
        self.user_request = user_request

    def exec(self, interviews: List[Interview]) -> EvaluationResult:
        if self.user_request is None:
            raise ValueError("User request is required.")

        try:
            prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                    "あなたは包括的な要件文書を作成するための情報の十分性を評価する専門家です。",
                ),
                (
                    "human",
                    "以下のユーザーリクエストとインタビュー結果に基づいて、包括的な要件文書を作成するのに十分な情報が集まったかどうかを判断してください。\n\n"
                    "ユーザーリクエスト: {user_request}\n\n"
                    "インタビュー結果:\n{interview_results}\n\n"
                    "以下の形式で回答してください：\n"
                    "{\n"
                    '  "reason": "判断の理由を詳細に記述してください",\n'
                    '  "is_sufficient": true または false\n'
                    "}"
                ),
            ])

            result: EvaluationResult = self.run(
                prompt,
                input_data={
                    "user_request": self.user_request,
                    "interview_results": self._format_interviews(interviews),
                },
            )
            self._print_evaluation(result)
            return result
        except Exception as e:
            iprint(f"情報の評価中にエラーが発生しました: {str(e)}")
            return EvaluationResult(reason="評価中にエラーが発生しました", is_sufficient=False)

    def _format_interviews(self, interviews: List[Interview]) -> str:
        return "\n".join(
            f"ペルソナ: {i.persona.name} - {i.persona.background}\n"
            f"質問: {i.question}\n回答: {i.answer}\n"
            for i in interviews
        )

    def _print_evaluation(self, result: EvaluationResult) -> None:
        gprint("評価結果:")
        gprint(f"情報の十分性: {'十分' if result.is_sufficient else '不十分'}")
        gprint(f"理由: {result.reason}")

if __name__ == "__main__":
    import argparse
    from agents.multi-agent.persona_generator import PersonaGenerator
    from agents.multi-agent.interview_conductor import InterviewConductor

    parser = argparse.ArgumentParser(description="ユーザー要求に基づいて情報の十分性を評価します")
    parser.add_argument("--task", type=str, help="作成したいアプリケーションについて記載してください")

    args = parser.parse_args()
    request = args.task or "新しいスマートホームアプリケーションの使いやすさについてのフィードバック"

    persona_generator = PersonaGenerator(user_request=request)
    personas = persona_generator.main()

    interviewer = InterviewConductor(user_request=request)
    interview_result = interviewer.main(personas.personas)

    evaluator = InformationEvaluator(user_request=request)
    evaluator.main(interview_result.interviews)

