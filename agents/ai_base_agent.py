from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from agents.base_agent import BaseAgent


class AIBaseAgent(BaseAgent):
    def __init__(self, agent_name: str, model_name: str = "gpt-4o-mini"):
        super().__init__(agent_name)
        self.model_name = model_name
        self.llm = ChatOpenAI(model=model_name, temperature=0.0)

    def main(self):
        raise NotImplementedError("Subclasses must implement main method")

    def run(self, messages) -> str:
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({})
