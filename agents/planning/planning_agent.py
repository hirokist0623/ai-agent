from ..base import BaseAgent
from langchain.prompts import ChatPromptTemplate


class PlanningAgent(BaseAgent):
    async def create_plan(self, goal: str) -> str:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたは目標達成のための多段階計画を立案するAIエージェントです。具体的で実行可能な計画を作成してください。",
                ),
                (
                    "human",
                    "以下の目標を達成するための5段階の計画を作成してください：\n\n{goal}",
                ),
            ]
        )

        return await self._process_prompt(prompt, goal=goal)
