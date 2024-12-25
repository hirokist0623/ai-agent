import yaml


def load_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def load_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
