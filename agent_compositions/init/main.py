import importlib

agents = [
    "agents.execution.git.branch_manager",
    "agents.planning.create_readme.structures.main",
    "agents.execution.git.commit_manager",
    "agents.execution.git.push_manager",
    "agents.execution.git.pr_creator",
]


def execute_agent(agent_path: str) -> None:
    print(f"\n\n[Executing agent] {agent_path}\n")

    try:
        module = importlib.import_module(agent_path)
        if hasattr(module, "main"):
            module.main()
        else:
            print(f"Warning: No main function found in {agent_path}.")
    except ImportError as e:
        print(f"Error: Failed to import agent {agent_path}. {e}")
    except Exception as e:
        print(f"Error: An error occurred while executing agent {agent_path}. {e}")


def main() -> None:
    index = 0
    try:
        while index < len(agents):
            execute_agent(agents[index])

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
    main()
