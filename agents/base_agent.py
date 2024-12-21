class BaseAgent:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name

    def main(self):
        raise NotImplementedError
