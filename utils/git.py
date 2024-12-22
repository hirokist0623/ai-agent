import os
import git


def get_git_root() -> str:
    try:
        repo = git.Repo(search_parent_directories=True)
        return repo.working_tree_dir
    except ImportError:
        print(
            "GitPython is not installed. ",
            "Using current directory as root.",
        )
        return os.getcwd()
    except git.InvalidGitRepositoryError:
        print("Not a git repository. Using current directory as root.")
        return os.getcwd()
