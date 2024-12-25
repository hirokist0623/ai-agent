import os
from utils.git import get_git_root

from utils.color_print import gprint


def clear_readme():
    readme_path = os.path.join(get_git_root(), "README.md")
    open(readme_path, "w", encoding="utf-8").close()
    gprint(f"README.md has been cleared at {readme_path}\n\n")


def append_to_readme(
    content: str, header: str = "## Header", file_path: str = ""
) -> None:
    readme_path = os.path.join(get_git_root(), file_path, "README.md")
    os.makedirs(os.path.dirname(readme_path), exist_ok=True)
    mode = "a" if os.path.exists(readme_path) else "w"

    with open(readme_path, mode, encoding="utf-8") as readme_file:
        if header:
            readme_file.write(f"\n\n{header}\n\n")
        readme_file.write(content)
        readme_file.write("\n")

    print(f"Content has been appended to {readme_path}\n")
    gprint(f"Content:\n{content}\n\n")
