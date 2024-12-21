import importlib
from typing import List


class AgentsBase:
    def __init__(self, agents: List[str] = None) -> None:
        self.agents: List[str] = agents

    def execute_agent(self, agent_path: str) -> None:
        print(f"\n\n[Executing agent] {agent_path}\n")

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

    def run(self) -> None:
        index = 0
        try:
            while index < len(self.agents):
                self.execute_agent(self.agents[index])

                while True:
                    try:
                        user_input = input(
                            "Do you want to proceed? [y/n/q]: "
                        ).lower()  # noqa
                        if user_input == "y":
                            index += 1
                            break
                        elif user_input == "n":
                            # Re-execute the current agent
                            break
                        elif user_input == "q":
                            print("Exiting the program.")
                            return
                        else:
                            print("Invalid input. Please enter y, n, or q.")
                    except KeyboardInterrupt:
                        print("\nProgram interrupted. Exiting.")
                        return

        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting.")


if __name__ == "__main__":
    agents_base = AgentsBase()
    agents_base.run()
