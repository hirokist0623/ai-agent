from typing import List, Tuple
import inquirer

from agent_compositions.agents_base import AgentsBase

from utils.color_print import iinput

AGENTS: List[Tuple[int, str, str]] = [
    (1, "1. commit supportor", "agent_compositions.simple_commit_agent"),
    (2, "2. branch manager", "agents.execution.git.branch_manager"),
    (3, "3. ai commit manager", "agents.execution.git.ai_commit_manager"),
    (4, "4. push manager", "agents.execution.git.push_manager"),
    (5, "5. pr creator", "agents.execution.git.pr_creator"),
    (6, "6. infra hearing agent", "agents.planning.infra.hearing_agent"),
    (
        7,
        "7. requirement document generator",
        "agents.planning.infra.requirements_document_generator",
    ),
]


class StartAgents(AgentsBase):
    def __init__(self):
        super().__init__([])

    def run(self) -> None:
        try:
            while True:
                agent_id = self.get_agent()
                agent = next(agent for agent in AGENTS if agent[0] == agent_id)[2]
                self.execute_agent(agent)

                confirmation = iinput(
                    "Do you want to continue using agents? (y/n): "
                ).lower()
                if confirmation in ["n", "no"]:
                    break
                print("Please choose next agent.")
        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting.")

    def get_agent(self) -> str:
        questions = [
            inquirer.List(
                "agent",
                message="Select an agent",
                choices=[(agent[1], agent[0]) for agent in AGENTS],
            ),
        ]
        answers = inquirer.prompt(questions)
        return answers["agent"]


if __name__ == "__main__":
    simple_commit_agent = StartAgents()
    simple_commit_agent.run()
