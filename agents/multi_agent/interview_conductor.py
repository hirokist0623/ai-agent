from typing import List

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from agents.ai_base_agent import AIBaseAgent
from agents.multi_agent.persona_generator import Persona, PersonaGenerator

from utils.color_print import gprint


class Interview(BaseModel):
    persona: Persona = Field(..., description="インタビュー対象のペルソナ")
    question: str = Field(..., description="インタビューでの質問")
    answer: str = Field(..., description="インタビューでの回答")


class InterviewResult(BaseModel):
    interviews: List[Interview] = Field(
        default_factory=list, description="インタビュー結果のリスト"
    )


class InterviewConductor(AIBaseAgent):
    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        user_request: str = None,
        personas: List[Persona] = None,
    ):
        super().__init__("InterviewConductor", model_name)
        self.user_request = user_request
        self.personas: List[Persona] = personas

    def exec(self) -> InterviewResult:
        if self.user_request is None:
            raise ValueError("User request is required.")

        try:
            questions = self._generate_questions()
            answers = self._generate_answers(questions)
            interviews = self._create_interviews(questions, answers)
            result = InterviewResult(interviews=interviews)
            self._print_interviews(result)
            return result
        except Exception as e:
            print(f"インタビュー実施中にエラーが発生しました: {str(e)}")
            return InterviewResult()

    def _generate_questions(self) -> List[str]:
        question_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたはユーザー要件に基づいて適切な質問を生成する専門家です。",
                ),
                (
                    "human",
                    "以下のペルソナに関連するユーザーリクエストについて、1つの質問を生成してください。\n\n"
                    "ユーザーリクエスト: {user_request}\n"
                    "ペルソナ: {persona_name} - {persona_background}\n\n"
                    "質問は具体的で、このペルソナの視点から重要な情報を引き出すように設計してください。",
                ),
            ]
        )
        question_chain = question_prompt | self.llm | StrOutputParser()

        question_queries = [
            {
                "user_request": self.user_request,
                "persona_name": persona.name,
                "persona_background": persona.background,
            }
            for persona in self.personas
        ]
        return question_chain.batch(question_queries)

    def _generate_answers(self, questions: List[str]) -> List[str]:
        answer_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "あなたは以下のペルソナとして回答しています: "
                        "{persona_name} - {persona_background}"
                    ),
                ),
                ("human", "質問: {question}"),
            ]
        )
        answer_chain = answer_prompt | self.llm | StrOutputParser()

        answer_queries = [
            {
                "persona_name": persona.name,
                "persona_background": persona.background,
                "question": question,
            }
            for persona, question in zip(self.personas, questions)
        ]
        return answer_chain.batch(answer_queries)

    def _create_interviews(
        self, questions: List[str], answers: List[str]
    ) -> List[Interview]:
        return [
            Interview(persona=persona, question=question, answer=answer)
            for persona, question, answer in zip(
                self.personas,
                questions,
                answers,
            )
        ]

    def _print_interviews(self, result: InterviewResult) -> None:
        for interview in result.interviews:
            gprint(f"ペルソナ: {interview.persona.name}")
            gprint(f"背景: {interview.persona.background}")
            gprint(f"質問: {interview.question}")
            gprint(f"回答: {interview.answer}")
            gprint("---")


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
    interviewer.main()
