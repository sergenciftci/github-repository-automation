""" a simple python module to initialize a repository on GitHub and clone it to your local machine

Raises:
    FileExistsError: when the repository already exists either on Github or on your local machine
    SystemExit: on any GitHub API request errors
    SystemExit: when another directory with the same name as the created repository already exists
"""
#!/usr/bin/env python3

import argparse
import os
import json
import requests
from dotenv import load_dotenv

GITHUB_API_URL = "https://api.github.com"


def validate_username_and_token(username: str, token: str):
    """

    Args:
        username (str): GitHub username
        token (str): GitHub token

    Raises:
        SystemExit: on any GitHub API request errors

    Returns:
        _type_: true when username matches login token
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.GitHub+json"
    }
    try:
        response = requests.get(url=f"{GITHUB_API_URL}/user", headers=headers)
        response.raise_for_status()
        if response.json()["login"] == username:
            return True
        else:
            print("Given token does not match username!")
    except requests.exceptions.RequestException as exc:
        raise SystemExit(exc) from exc


def init_repository(repository_name: str,
                    username: str,
                    token: str,
                    path: str,
                    public: bool = False):
    """initializes repository on GitHub

    Args:
        repository_name (str):
        username (str): GitHub username
        token (str): GitHub token with repository create permissions
        path (str): base path where the repository will be created
        public (bool, optional): repository visibility on GitHub. Defaults to False.

    Raises:
        SystemExit: on any GitHub API request errors
    """
    payload = {
        "name": repository_name,
        "private": not public,
        "auto_init": True
    }
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.GitHub+json"
    }
    try:
        response = requests.get(
            url=f"{GITHUB_API_URL}/repos/{username}/{repository_name}",
            headers=headers)
        if response.status_code == 200:
            raise FileExistsError(
                f"\"{repository_name}\" already exists on your GitHub profile."
            )
        response = requests.post(url=f"{GITHUB_API_URL}/user/repos",
                                 data=json.dumps(payload),
                                 headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise SystemExit(exc) from exc
    clone_repository(username=username,
                     path=path,
                     repository_name=repository_name,
                     token=token)


def clone_repository(username: str, path: str, repository_name: str,
                     token: str):
    """

    Args:
        username (str): GitHub username
        path (str): base path where the repository will be created
        repository_name (str): repository visibility on GitHub. Defaults to False.

    Raises:
        SystemExit: when another directory with the same name as the created repository
        already exists
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            print(f"Created directory {path}")
        os.chdir(path)
        os.system(
            f"git clone https://{username}:{token}@github.com/{username}/{repository_name}.git"
        )
    except FileExistsError as exc:
        raise SystemExit(exc) from exc


def main():
    """
    handles argument validation
    """
    parser = argparse.ArgumentParser(
        description=
        "a simple script that initializes a repository on GitHub and your local machine"
    )
    parser.add_argument("-n",
                        "--repository-name",
                        required=True,
                        type=str,
                        help="repository name")
    parser.add_argument("-u",
                        "--username",
                        required=False,
                        type=str,
                        help="GitHub username, can also be stored in .env")
    parser.add_argument("-t",
                        "--token",
                        required=False,
                        type=str,
                        help="GitHub token, can also be stored in .env")
    parser.add_argument(
        "-p",
        "--path",
        required=False,
        type=str,
        help="base path for the repository, can also be stored in .env")
    parser.add_argument("--public", dest="is_public", action="store_true")
    args = parser.parse_args()
    load_dotenv()
    if args.username is None:
        username = os.environ.get("GITHUB_USERNAME")
    else:
        username = args.username
    if args.token is None:
        token = os.environ.get("GITHUB_TOKEN")
    else:
        token = args.token
    if args.path is None:
        path = os.environ.get("PROJECTS_BASE_PATH")
    else:
        path = args.path
    if not username:
        print(
            "Missing username argument. Store your username in .env USERNAME or pass it as \"-u\" "
            "argument, when running this script.")
        return
    if not token:
        print(
            "Missing GitHub token argument. Store your token in .env TOKEN or pass it as \"-t\" "
            "argument, when running this script.")
        return
    if not path:
        print(
            "Missing path argument. Store your base path for the new repositories to created in "
            ".env PATH or pass it as \"-p\" argument, when running this script."
        )
        return
    validate_username_and_token(username=username, token=token)
    init_repository(repository_name=args.repository_name,
                    username=username,
                    token=token,
                    path=path,
                    public=args.is_public)


if __name__ == "__main__":
    main()
