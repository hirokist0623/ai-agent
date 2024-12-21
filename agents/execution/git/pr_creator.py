import os
import sys
import subprocess
import requests


def get_current_repo():
    try:
        remote_url = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"],
            universal_newlines=True,
        ).strip()
        if remote_url.endswith(".git"):
            remote_url = remote_url[:-4]
        if remote_url.startswith("https://github.com/"):
            return remote_url[19:]
        elif remote_url.startswith("git@github.com:"):
            return remote_url[15:]
        else:
            print("Error: Unable to parse GitHub repository from remote URL.")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print(
            "Error: Unable to get git remote URL. "
            "Make sure you're in a git repository."
        )
        sys.exit(1)


def get_current_branch():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            universal_newlines=True,
        ).strip()
    except subprocess.CalledProcessError:
        print("Error: Unable to get current branch name.")
        sys.exit(1)


def format_pr_title(branch_name):
    # Remove 'feature/' prefix if present
    if branch_name.startswith("feature/"):
        branch_name = branch_name[8:]

    # Split by underscores or hyphens
    parts = branch_name.replace("-", " ").replace("_", " ").split()

    # Capitalize each word, except the first one
    return parts[0] + " " + " ".join(word.capitalize() for word in parts[1:])


def get_pr_template():
    template_path = ".github/pull_request_template.md"
    if os.path.exists(template_path):
        with open(template_path, "r") as file:
            return file.read()
    else:
        print("Warning: PR template not found. Using empty body.")
        return ""


def check_existing_pr(repo, head):
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable is not set.")
        sys.exit(1)

    url = f"https://api.github.com/repos/{repo}/pulls"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    params = {"state": "open", "head": f"{repo.split('/')[0]}:{head}"}

    response = requests.get(url, headers=headers, params=params, timeout=10)

    if response.status_code == 200:
        prs = response.json()
        for pr in prs:
            if pr["head"]["ref"] == head:
                pr_url = pr["html_url"]
                print(f"A pull request already exists for this branch: {pr_url}")
                return True
    else:
        print(f"Error checking existing pull requests: {response.status_code}")
        print(response.text)
        sys.exit(1)

    return False


def create_pull_request(repo, base, head, title, body):
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable is not set.")
        sys.exit(1)

    url = f"https://api.github.com/repos/{repo}/pulls"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {"title": title, "body": body, "head": head, "base": base}

    response = requests.post(url, headers=headers, json=data, timeout=10)

    if response.status_code == 201:
        pr_url = response.json()["html_url"]
        print(f"Pull request created successfully: {pr_url}")
    else:
        print(f"Error creating pull request: {response.status_code}")
        print(response.text)


def main():
    repo = get_current_repo()
    base = "main"
    head = get_current_branch()
    title = format_pr_title(head)

    print(f"Repository: {repo}")
    print(f"Base branch: {base}")
    print(f"Head branch: {head}")
    print(f"PR title: {title}")

    # Check if PR already exists
    if check_existing_pr(repo, head):
        print("Skipping PR creation as one already exists.")
        return

    # Get PR body from template
    body = get_pr_template()
    print("\nPR body template:")
    print(body)

    # Allow user to edit the PR body
    print("\nYou can edit the PR body. Press Enter twice when finished:")
    user_input = "\n".join(iter(input, ""))
    if user_input:
        body = user_input

    create_pull_request(repo, base, head, title, body)


if __name__ == "__main__":
    main()
