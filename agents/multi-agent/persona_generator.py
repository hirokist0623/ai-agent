from typing import List

from pydantic import BaseModel, Field

from agents.ai_base_agent import AIBaseAgent


class Persona(BaseModel):
    name: str = Field(..., description="ペルソナの名前")
    background: str = Field(..., description="ペルソナの簡単な背景")


class Personas(BaseModel):
    personas: List[Persona] = Field(..., description="生成されたペルソナのリスト")


class PersonaGenerator(AIBaseAgent):
    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        user_request: str = None,
    ):
        super().__init__("PersonaGenerator", model_name)
        self.user_request = user_request

    def exec(self):
        if self.user_request is None:
            raise ValueError("User request is required.")

        messages = [
            (
                "system",
                "あなたはユーザーインタビュー用の多様なペルソナを作成する専門家です。",
            ),
            (
                "human",
                f"以下のユーザーリクエストに関するインタビュー用に、{self.k}人の多様なペルソナを生成してください。\n\n"
                "ユーザーリクエスト: {user_request}\n\n"
                "各ペルソナには名前と簡単な背景を含めてください。年齢、性別、職業、技術的専門知識において多様性を確保してください。",
            ),
        ]

        exec_result = self.run(
            messages,
            input_data={"user_request": self.user_request},
        )

        personas = Personas(personas=[Persona(**p) for p in eval(exec_result)])

        for persona in personas:
            print(f"名前: {persona.name}")
            print(f"背景: {persona.background}")
            print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="ユーザー要求に基づいてペルソナを生成します"
    )
    parser.add_argument(
        "--task",
        type=str,
        help="作成したいアプリケーションについて記載してください",
    )

    request = (
        parser.parse_args().task
        or "新しいスマートホームアプリケーションの使いやすさについてのフィードバック"
    )
    generator = PersonaGenerator(user_request=request)
    generator.main()
