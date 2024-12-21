import importlib

agents = ["agents.planning.create_readme.structures.main"]


def execute_agent(agent_path: str) -> None:
    print(f"Executing agent: {agent_path}")

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
    while index < len(agents):
        execute_agent(agents[index])

        while True:
            user_input = input("Do you want to proceed? [y/n/q]: ").lower()
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

    print("All agents have been executed.")


if __name__ == "__main__":
    main()
