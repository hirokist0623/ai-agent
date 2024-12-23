from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from agents.base_agent import BaseAgent
from utils.color_print import cprint


class AIBaseAgent(BaseAgent):
    def __init__(self, agent_name: str, model_name: str = "gpt-4o-mini"):
        super().__init__(agent_name)
        self.model_name = model_name
        self.llm = ChatOpenAI(model=model_name, temperature=0.0)

    def main(self):
        cprint("######################################")
        cprint(f"# Running AI Agent: {self.agent_name}...")
        cprint("#######################################\n")
        self.exec()

    def exec(self):
        raise NotImplementedError("Subclasses must implement main method")

    def run(self, messages, input_data: dict = None) -> str:
        if input_data is None:
            input_data = {}
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke(input_data)
