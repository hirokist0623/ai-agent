from agent_compositions.agents_base import AgentsBase


class ReadmeCreatorAgent(AgentsBase):
    def __init__(self):
        super().__init__(
            [
                "agents.execution.scan_directory_structure",
                "agents.execution.readme.reset_readme",
                "agents.execution.readme.create_structure",
            ]
        )


if __name__ == "__main__":
    agent = ReadmeCreatorAgent()
    agent.run()
