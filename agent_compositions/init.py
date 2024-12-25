from agent_compositions.agents_base import AgentsBase


class ReadmeCreatorAgent(AgentsBase):
    def __init__(self):
        super().__init__(
            [
                "agents.execution.git.branch_manager",
                "agents.execution.init_config.create_config",
                "agents.execution.git.create_template",
                "agents.execution.git.ai_commit_manager",
                "agents.execution.git.push_manager",
                "agents.execution.git.pr_creator",
            ]
        )


if __name__ == "__main__":
    agent = ReadmeCreatorAgent()
    agent.run()
