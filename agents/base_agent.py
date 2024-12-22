from utils.color_print import cprint


class BaseAgent:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name

    def main(self):
        cprint("######################################")
        cprint(f"# Running Agent: {self.agent_name}...")
        cprint("#######################################\n")
        self.exec()

    def exec(self):
        raise NotImplementedError
