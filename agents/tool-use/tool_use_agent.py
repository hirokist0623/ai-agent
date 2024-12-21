from ..base import BaseAgent
from langchain.prompts import ChatPromptTemplate
from langchain.tools import BaseTool
from typing import List


class ToolUseAgent(BaseAgent):
    def __init__(self, llm, tools: List[BaseTool]):
        super().__init__(llm)
        self.tools = tools

    async def use_tool(self, task: str) -> str:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたは与えられたツールを使用してタスクを解決するAIエージェントです。適切なツールを選択し、使用してください。",
                ),
                (
                    "human",
                    "以下のタスクを解決するために、最適なツールを選択し使用してください：\n\n{task}\n\n利用可能なツール：\n{tool_descriptions}",
                ),
            ]
        )

        tool_descriptions = "\n".join(
            [f"- {tool.name}: {tool.description}" for tool in self.tools]
        )

        return await self._process_prompt(
            prompt, task=task, tool_descriptions=tool_descriptions
        )
