"""This module contains functions for retrieving and filtering help-wanted issues from GitHub."""
import re
import os
import requests
from dotenv import load_dotenv


load_dotenv()
USERNAME = os.getenv("MY_USERNAME")
token    = os.getenv("TOKEN")


headers      = {"Authorization": f"token {token}"}
labels       = 'good first issue,help wanted'
label_list   = labels.split(',')
issue_titles = []


def get_help_wanted_issues():
    """
    Retrieves and filters help-wanted issues from GitHub.

    Returns:
        A list of issue titles.
    """
    print("MY_USERNAME:", USERNAME)
    print("TOKEN:", token)

    if USERNAME is None:
        raise ValueError("USERNAME not set in .env file")
    
    issue_titles.clear()

    for repo_name in get_repositories(USERNAME, headers):
        open_issues     = get_open_issues(repo_name, headers, label_list)
        if open_issues is not None:
            relevant_issues = filter_relevant_issues(open_issues)
            issues          = [issue['title'] for issue in relevant_issues]
            issue_titles.extend(issues)

def get_repositories(USERNAME, headers):
    """
    Retrieves a list of repositories that the specified user has starred on GitHub.

    Args:
        USERNAME (str): The GitHub USERNAME of the user whose starred repositories will be retrieved.
        headers (dict): A dictionary containing the authorization token for the GitHub API.

    Returns:
        A list of repository names in the format "USERNAME/repo_name".
    """

    url = f"https://api.github.com/users/{USERNAME}/starred"
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    repositories = [repo["full_name"] for repo in response.json()]
    return repositories


def get_open_issues(repo_name, headers, labels):
    """
    Retrieves a list of open issues for the specified repository and labels.

    Args:
        repo_name (str): The name of the repository in the format "USERNAME/repo_name".
        headers (dict) : A dictionary containing the authorization token for the GitHub API.
        labels (list)  : A list of labels to filter the issues by.

    Returns:
        A list of open issues for the specified repository and labels.
    """
    issues = []
    repo_info = requests.get(f'https://api.github.com/repos/{repo_name}', headers=headers, timeout=10).json()
    if not repo_info.get('archived', False): # check if repository is not archived
        for label in labels:
            url      = f'https://api.github.com/repos/{repo_name}/issues'
            params   = {'state': 'open', 'labels': label}
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                issues.extend(response.json())
                if issues:
                    print(f"Repository '{repo_name}' (https://github.com/{repo_name}) has {len([issue for issue in issues if not re.search(r'fixed|fixed_in_dev', ', '.join(label['name'] for label in issue['labels']))])} open issues labeled '{label}'")
                    for issue in issues:
                        issue_titles.append(issue['title'])
                #else:
                # print(f"Skipping archived repository '{repo_name}'")
        if issues:
            return issues
    return None


def filter_relevant_issues(issues):
    """
    Filters a list of issues to remove those that have the 'fixed' or 'fixed_in_dev' label.

    Args:
        issues (list): A list of issues to filter.

    Returns:
        A list of issues that do not have the 'fixed' or 'fixed_in_dev' label.
    """
    relevant_issues = []
    for issue in issues:
        labels = [label['name'] for label in issue['labels']]
        if not any(label in labels for label in ['fixed', 'fixed_in_dev']):
            relevant_issues.append(issue)
    return relevant_issues


get_help_wanted_issues()
