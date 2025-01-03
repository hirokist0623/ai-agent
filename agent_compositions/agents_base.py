import importlib
from typing import List

from agents.base_agent import BaseAgent


class AgentsBase(BaseAgent):
    def __init__(self, agents: List[str] = None) -> None:
        super().__init__("AgentsBase")
        self.agents: List[str] = agents

    def exec(self) -> None:
        index = 0
        try:
            while index < len(self.agents):
                self.execute_agent(self.agents[index])
                index += 1
        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting.")

    def execute_agent(self, agent_path: str) -> None:
        try:
            module = importlib.import_module(agent_path)
            if hasattr(module, "main"):
                module.main()
            elif hasattr(module, "__dict__"):
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type) and hasattr(obj, "main"):
                        # クラスをインスタンス化する際に引数を渡さないようにする
                        if (
                            hasattr(obj, "__init__")
                            and obj.__init__.__code__.co_argcount == 1
                        ):
                            instance = obj()
                        else:
                            print(
                                f"Warning: Class {name} in {agent_path} "
                                f"requires arguments for initialization. "
                                f"Skipping.\n"
                            )
                            continue
                        instance.main()
                        break
                else:
                    print(
                        f"Warning: No main function "
                        f"or class with main msethod found in "
                        f"{agent_path}."
                    )
            else:
                print(f"Warning: No main function found in {agent_path}.")
        except ImportError as e:
            print(f"Error: Failed to import agent {agent_path}. {e}")
        except Exception as e:
            print(
                f"Error: "
                f"An error occurred while executing agent {agent_path}."
                f"{e}"  # noqa
            )


if __name__ == "__main__":
    agents_base = AgentsBase()
    agents_base.main()
