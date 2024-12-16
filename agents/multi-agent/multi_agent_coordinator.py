# agents/multi_agent/multi_agent_coordinator.py

from ..base import BaseAgent
from langchain.prompts import ChatPromptTemplate
from typing import List


class MultiAgentCoordinator(BaseAgent):
    async def coordinate_agents(self, task: str, available_agents: List[str]) -> str:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたは複数のAIエージェントを調整し、協調してタスクを解決するコーディネーターです。最適なエージェントの組み合わせと作業順序を決定してください。",
                ),
                (
                    "human",
                    "以下のタスクを解決するために、利用可能なエージェントの中から最適な組み合わせと作業順序を決定してください：\n\nタスク：{task}\n\n利用可能なエージェント：\n{agent_list}",
                ),
            ]
        )

        agent_list = "\n".join([f"- {agent}" for agent in available_agents])

        return await self._process_prompt(prompt, task=task, agent_list=agent_list)
