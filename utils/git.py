import os
from urllib.parse import urlparse

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


def get_github_url() -> str:
    repo = git.Repo(search_parent_directories=True)
    remote_url = repo.remotes.origin.url
    print(f"Remote URL: {remote_url}")
    parsed_url = urlparse(remote_url)
    print(f"Remote URL: {parsed_url}")
    if parsed_url.scheme == "https":
        print(f"parsed_url.path: {parsed_url.scheme}")
        print(f"ssh_path: {remote_url}")
        return remote_url.rstrip(".git")
    elif parsed_url.scheme == "git":
        print(f"parsed_url.scheme: {parsed_url.scheme}")
        print(f"parsed_url.scheme: {parsed_url.path}")
        return f"https://github.com{parsed_url.path}".rstrip(".git")
    else:
        # SSHの場合
        ssh_path = parsed_url.path.split(":", 1)[-1]
        print(f"parsed_url.path: {parsed_url.path}")
        print(f"ssh_path: {ssh_path}")
        return f"https://github.com/{ssh_path}".rstrip(".git")


def get_commit_hash() -> str:
    repo = git.Repo(search_parent_directories=True)
    return repo.head.commit.hexsha


def git_commit_url() -> str:
    commit_hash = get_commit_hash()
    print(f"Commit URL: {get_github_url()}")
    return f"{get_github_url()}/commit/{commit_hash}"
