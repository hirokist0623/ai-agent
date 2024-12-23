from agent_compositions.agents_modern_base import AgentsBase


class SpecificationWriterAgent(AgentsBase):
    def __init__(self):
        super().__init__(
            [
                # "agents.execution.git.branch_manager",
            ]
        )


if __name__ == "__main__":
    simple_commit_agent = SpecificationWriterAgent()
    simple_commit_agent.run()
