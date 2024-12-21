import argparse
from utils.load_yaml import load_yaml


def replace_project_name(structure, project_name):
    return structure.replace("${projectName}", project_name)


def main():
    parser = argparse.ArgumentParser(description="Generate project structure")
    parser.add_argument("project_name", help="Name of the project")
    args = parser.parse_args()

    yaml_path = "agents/planning/create_readme/structures/yaml/infra.yaml"
    structure_data = load_yaml(yaml_path)

    structure = structure_data["structure"]
    structure_with_project_name = replace_project_name(structure, args.project_name)

    print(structure_with_project_name)


if __name__ == "__main__":
    main()
