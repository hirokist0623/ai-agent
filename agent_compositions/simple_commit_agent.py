from agent_compositions.agents_base import AgentsBase


class SimpleCommitAgent(AgentsBase):
    def __init__(self):
        super().__init__(
            [
                "agents.execution.git.branch_manager",
                "agents.execution.git.ai_commit_manager",
                "agents.execution.git.push_manager",
                "agents.execution.git.pr_creator",
            ]
        )


if __name__ == "__main__":
    simple_commit_agent = SimpleCommitAgent()
    simple_commit_agent.main()
