# agents/reflection/reflection_agent.py

from ..base_agent import BaseAgent
from langchain.prompts import ChatPromptTemplate


class ReflectionAgent(BaseAgent):
    async def reflect(self, past_performance: str) -> str:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたは自己改善プロセスを行うAIエージェントです。過去のパフォーマンスを分析し、改善点を提案してください。",
                ),
                (
                    "human",
                    "以下の過去のパフォーマンスを分析し、改善点を3つ挙げてください：\n\n{past_performance}",
                ),
            ]
        )

        return await self._process_prompt(prompt, past_performance=past_performance)
