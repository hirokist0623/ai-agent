import os
import sys
from utils.load_yaml import load_yaml


def replace_project_name(structure, project_name):
    return structure.replace("${projectName}", project_name)


def main():
    project_name = sys.argv[1] if len(sys.argv) > 1 else "default_project"
    script_dir = os.path.dirname(os.path.abspath(__file__))

    yaml_path = os.path.join(script_dir, "yaml", "infra.yaml")
    structure_data = load_yaml(yaml_path)

    structure = structure_data["structure"]
    structure_with_project_name = replace_project_name(structure, project_name)

    print(structure_with_project_name)


if __name__ == "__main__":
    main()
