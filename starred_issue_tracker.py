"""This module contains functions for retrieving and filtering help-wanted issues from GitHub."""
import re
import os
from dotenv import load_dotenv
import requests


def get_help_wanted_issues():
    """
    Retrieves a list of open issues with labels from your starred repositories.

    Returns:
    A list of issue titles.
    """
    load_dotenv() # charger les variables depuis le fichier .env

    # récupérer les valeurs des variables
    username = os.getenv("GITHUB_USERNAME")
    token    = os.getenv("TOKEN")

    print("GITHUB_USERNAME:", username)
    print("TOKEN:", token)

    # check that username is not None
    if username is None:
        raise ValueError("Username not set in .env file")
    
    # retrieve a list of your starred repositories
    repositories = get_starred_repositories(username, token)

    # search for issues with specified labels in each repository
    labels       = 'good first issue,help wanted'
    issue_titles = get_issues_with_labels(repositories, labels, token)

    return issue_titles

def get_starred_repositories(username, token):
    """
    Retrieves a list of repositories that the specified user has starred on GitHub.

    Args:
        username (str): The GitHub username of the user whose starred repositories will be retrieved.
        token (str)   : The personal access token for the user's GitHub account.

    Returns:
        A list of strings, where each string is the full name of a repository that the user has starred.
    """
    url      = f"https://api.github.com/users/{username}/starred"
    headers  = {"Authorization": f"token {token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        repositories = [repo["full_name"] for repo in response.json()]

        return repositories
    
    except requests.exceptions.RequestException as error:
        print("Error retrieving repositories:", error)
        return []

def is_archived_repository(repo_name, token):
    """
    Determines whether a repository is archived or not.

    Args:
        repo_name (str): The name of the repository to check.
        token (str)    : The personal access token for the user's GitHub account.

    Returns:
        A boolean value indicating whether the repository is archived or not.
    """
    repo_info = requests.get(f'https://api.github.com/repos/{repo_name}', headers={"Authorization": f"token {token}"}, timeout=10).json()
    return repo_info.get('archived', False)

def get_issues_for_label(repo_name, label, token):
    """
    Retrieves a list of open issues from a specified repository that have a specified label.

    Args:
        repo_name (str): The name of the repository to retrieve issues from.
        label (str)    : The label to filter issues by.
        token (str)    : The personal access token for the user's GitHub account.

    Returns:
        A list of dictionaries, where each dictionary represents an open issue with the specified label.
    """
    response = requests.get(f'https://api.github.com/repos/{repo_name}/issues', 
                            headers={"Authorization": f"token {token}"},
                            params={'state': 'open', 'labels': label}, timeout=10)
    issues = response.json()
    return issues

def get_open_issues(issues):
    """
    Returns a list of open issues that do not have the labels 'fixed' or 'fixed_in_dev'.

    Args:
        issues (list): A list of dictionaries, where each dictionary represents an open issue.

    Returns:
        A list of dictionaries, where each dictionary represents an open issue that does not have the labels 'fixed' or 'fixed_in_dev'.
    """
    return [issue for issue in issues if not re.search(r'fixed|fixed_in_dev', ', '.join(label['name'] for label in issue['labels']))]

def get_issues_with_labels(repositories, labels, token):
    """
    Retrieves a list of open issues from the specified repositories that have the specified labels.

    Args:
        repositories (list): A list of repository names to retrieve issues from.
        labels (str)       : A comma-separated string of labels to filter issues by.
        token (str)        : The personal access token for the user's GitHub account.

    Returns:
        A list of issue titles.
    """
    issue_titles = []
    for repo_name in repositories:
        if not is_archived_repository(repo_name, token):
            for label in labels.split(','):
                issues = get_issues_for_label(repo_name, label, token)
                if issues:
                    print(f"Repository '{repo_name}' (https://github.com/{repo_name}) has {len(get_open_issues(issues))} open issues labeled '{label}'")
                    for issue in get_open_issues(issues):
                        issue_titles.append(issue['title'])
        else:
            print(f"Skipping archived repository '{repo_name}'")
    return issue_titles

get_help_wanted_issues()
