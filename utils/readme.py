import os
from utils.git import get_git_root


def clear_readme():
    readme_path = os.path.join(get_git_root(), "README.md")
    open(readme_path, "w", encoding="utf-8").close()
    print(f"README.md has been cleared at {readme_path}")


def append_to_readme(content: str, header: str = "## Header") -> None:
    readme_path = os.path.join(get_git_root(), "README.md")
    with open(readme_path, "a", encoding="utf-8") as readme_file:
        if header:
            readme_file.write(f"\n\n{header}\n\n")
            if not content.startswith("```"):
                readme_file.write("```\n")
        readme_file.write(content)
        if header and not content.endswith("```"):
            readme_file.write("\n```")
        readme_file.write("\n")

    print(f"\nContent has been appended to {readme_path}")
