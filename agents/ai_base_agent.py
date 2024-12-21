from agents.base_agent import BaseAgent


class AIBaseAgent(BaseAgent):
    def __init__(self, agent_name: str, model_name: str = "gpt-4o-mini"):
        super().__init__(agent_name)
        self.model_name = model_name

    def main(self):
        raise NotImplementedError("Subclasses must implement main method")
