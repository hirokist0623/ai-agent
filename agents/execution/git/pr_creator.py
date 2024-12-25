import os
import sys
import subprocess
import requests
import inquirer

from agents.base_agent import BaseAgent

from utils.color_print import gprint


class PRCreator(BaseAgent):
    def __init__(self):
        super().__init__("PRCreator")

    def exec(self):
        repo = self.get_current_repo()
        base = "main"
        head = self.get_current_branch()
        title = self.format_pr_title(head)

        gprint(f"Repository: {repo}")
        gprint(f"Base branch: {base}")
        gprint(f"Head branch: {head}")
        gprint(f"PR title: {title}")

        # Check if PR already exists
        if self.check_existing_pr(repo, head):
            print("Skipping PR creation as one already exists.")
            return

        # Get PR body from template
        body = self.get_pr_template()
        gprint("PR body template:")
        gprint(body)

        # Ask for confirmation of the PR body
        confirmation = self.get_confirmation()
        if confirmation != "confirm":
            print("PR creation cancelled.")
            return

        pr_url = self.create_pull_request(repo, base, head, title, body)
        if pr_url:
            gprint(f"Pull request created successfully. PR URL: {pr_url}")

    def get_current_repo(self):
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

    def get_current_branch(self):
        try:
            return subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                universal_newlines=True,
            ).strip()
        except subprocess.CalledProcessError:
            print("Error: Unable to get current branch name.")
            sys.exit(1)

    def format_pr_title(self, branch_name):
        parts = branch_name.split("/", 1)

        prefix = parts[0].capitalize() if len(parts) > 1 else "Feature"
        remaining = parts[1] if len(parts) > 1 else branch_name

        capitalized_remaining = " ".join(
            word.lower() for word in remaining.split("_")
        )  # noqa

        return f"{prefix}/{capitalized_remaining}"

    def get_pr_template(self):
        template_path = ".github/pull_request_template.md"
        if os.path.exists(template_path):
            with open(template_path, "r", encoding="utf-8") as file:
                return file.read()
        else:
            print("Warning: PR template not found. Using empty body.")
            return ""

    def check_existing_pr(self, repo, head):
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
                    print(
                        f"A pull request already exists for this branch: {pr_url}"  # noqa
                    )
                    return True
        else:
            print(
                f"Error checking existing pull requests: {response.status_code}"  # noqa
            )
            print(response.text)
            sys.exit(1)

        return False

    def create_pull_request(self, repo, base, head, title, body):
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
            return response.json()["html_url"]
        else:
            print(f"Error creating pull request: {response.status_code}")
            print(response.text)
            return None

    def get_confirmation(self) -> str:
        questions = [
            inquirer.List(
                "action",
                message="Is this PR body template okay?",
                choices=[
                    ("Yes, create PR", "confirm"),
                    ("No, cancel", "cancel"),
                ],
            ),
        ]
        answers = inquirer.prompt(questions)
        return answers["action"]


if __name__ == "__main__":
    pr_creator = PRCreator()
    pr_creator.exec()
