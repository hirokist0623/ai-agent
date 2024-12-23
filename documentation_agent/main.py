import operator
from typing import Annotated, Any, Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field

from agents.multi_agent.persona_generator import (
    Persona,
    Personas,
    PersonaGenerator,
)
from agents.multi_agent.interview_conductor import (
    Interview,
    InterviewResult,
    InterviewConductor,
)
from agents.multi_agent.information_evaluator import (
    EvaluationResult,
    InformationEvaluator,
)
from agents.planning.requirements_document_generator import (
    RequirementsDocumentGenerator,
)


# .envファイルから環境変数を読み込む
load_dotenv()


# 要件定義生成AIエージェントのステート
class InterviewState(BaseModel):
    user_request: str = Field(..., description="ユーザーからのリクエスト")
    personas: Annotated[list[Persona], operator.add] = Field(
        default_factory=list, description="生成されたペルソナのリスト"
    )
    interviews: Annotated[list[Interview], operator.add] = Field(
        default_factory=list, description="実施されたインタビューのリスト"
    )
    requirements_doc: str = Field(default="", description="生成された要件定義")
    iteration: int = Field(
        default=0, description="ペルソナ生成とインタビューの反復回数"
    )
    is_information_sufficient: bool = Field(
        default=False, description="情報が十分かどうか"
    )


# 要件定義書生成AIエージェントのクラス
class DocumentationAgent:
    def __init__(
        self, llm: ChatOpenAI, k: Optional[int] = None, user_request: str = ""
    ):
        # 各種ジェネレータの初期化
        self.llm = llm
        self.k = k
        self.user_request = user_request

        self.result: dict = {}

        # グラフの作成
        self.graph = self._create_graph()

    def _create_graph(self) -> StateGraph:
        # グラフの初期化
        workflow = StateGraph(InterviewState)

        # 各ノードの追加
        workflow.add_node("generate_personas", self._generate_personas)
        workflow.add_node("conduct_interviews", self._conduct_interviews)
        workflow.add_node("evaluate_information", self._evaluate_information)
        workflow.add_node("generate_requirements", self._generate_requirements)

        # エントリーポイントの設定
        workflow.set_entry_point("generate_personas")

        # ノード間のエッジの追加
        workflow.add_edge("generate_personas", "conduct_interviews")
        workflow.add_edge("conduct_interviews", "evaluate_information")
        # 条件付きエッジの追加
        workflow.add_conditional_edges(
            "evaluate_information",
            lambda state: not state.is_information_sufficient and state.iteration < 5,
            {True: "generate_personas", False: "generate_requirements"},
        )
        workflow.add_edge("generate_requirements", END)

        # グラフのコンパイル
        return workflow.compile()

    def _generate_personas(self, state: InterviewState) -> dict[str, Any]:
        # ペルソナの生成
        persona_generator = PersonaGenerator(
            user_request=self.user_request,
            persona_num=self.k,
        )
        new_personas: Personas = persona_generator.main()
        return {
            "personas": new_personas.personas,
            "iteration": state.iteration + 1,
        }

    def _conduct_interviews(self, state: InterviewState) -> dict[str, Any]:
        # インタビューの実施
        interview_conductor = InterviewConductor(
            user_request=state.user_request,
            personas=state.personas[-5:],
        )
        new_interviews: InterviewResult = interview_conductor.main()
        return {"interviews": new_interviews.interviews}

    def _evaluate_information(self, state: InterviewState) -> dict[str, Any]:
        # 情報の評価
        information_evaluator = InformationEvaluator(
            user_request=state.user_request,
            interviews=state.interviews,
        )
        evaluation_result: EvaluationResult = information_evaluator.main()
        return {
            "is_information_sufficient": evaluation_result.is_sufficient,
            "evaluation_reason": evaluation_result.reason,
        }

    def _generate_requirements(self, state: InterviewState) -> dict[str, Any]:
        # 要件定義書の生成
        requirements_generator = RequirementsDocumentGenerator(
            user_request=state.user_request,
            interviews=state.interviews,
        )
        requirements_doc: str = requirements_generator.main()
        return {"requirements_doc": requirements_doc}

    def run(self, user_request: str) -> str:
        # 初期状態の設定
        initial_state = InterviewState(user_request=user_request)
        # グラフの実行
        final_state = self.graph.invoke(initial_state)
        # 最終的な要件定義書の取得
        return final_state["requirements_doc"]


# 実行方法:
# poetry run python -m documentation_agent.main --task "ユーザーリクエストをここに入力してください"
# 実行例）
# poetry run python -m documentation_agent.main --task "スマートフォン向けの健康管理アプリを開発したい"
def main():
    import argparse

    # コマンドライン引数のパーサーを作成
    parser = argparse.ArgumentParser(
        description="ユーザー要求に基づいて要件定義を生成します"
    )
    # "task"引数を追加
    parser.add_argument(
        "--task",
        type=str,
        help="作成したいアプリケーションについて記載してください",
    )
    # "k"引数を追加
    parser.add_argument(
        "--k",
        type=int,
        default=3,
        help="生成するペルソナの人数を設定してください（デフォルト:3）",
    )
    # コマンドライン引数を解析
    args = parser.parse_args()

    # ChatOpenAIモデルを初期化
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    # 要件定義書生成AIエージェントを初期化
    agent = DocumentationAgent(llm=llm, k=args.k, user_request=args.task)
    # エージェントを実行して最終的な出力を取得
    final_output = agent.run(user_request=args.task)

    # 最終的な出力を表示
    print(final_output)


if __name__ == "__main__":
    main()
