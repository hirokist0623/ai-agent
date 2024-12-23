from typing import Optional, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from agents.base_agent import BaseAgent
from utils.color_print import cprint


class AIBaseAgent(BaseAgent):
    def __init__(
        self,
        agent_name: str,
        model_name: str = "gpt-4o-mini",
        output_type: Optional[type] = None,
    ):
        super().__init__(agent_name)
        self.model_name = model_name
        self.llm = ChatOpenAI(model=model_name, temperature=0.0)
        self.output_type = output_type
        if output_type:
            self.llm = self.llm.with_structured_output(output_type)

    def main(self):
        cprint("######################################")
        cprint(f"# Running AI Agent: {self.agent_name}...")
        cprint("#######################################\n")
        return self.exec()

    def exec(self) -> Any:
        raise NotImplementedError("Subclasses must implement exec method")

    def run(self, messages, input_data: dict = None) -> Any:
        if input_data is None:
            input_data = {}
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | self.llm
        return chain.invoke(input_data)
