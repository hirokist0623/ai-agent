# agents/base_agent.py

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


class BaseAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    async def _process_prompt(self, prompt: ChatPromptTemplate, **kwargs):
        chain = prompt | self.llm
        result = await chain.ainvoke(kwargs)
        return result.content
