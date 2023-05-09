import re
import os
from dotenv import load_dotenv
import requests


def get_help_wanted_issues():
    load_dotenv() # charger les variables depuis le fichier .env

    # récupérer les valeurs des variables
    username = os.getenv("MY_USERNAME")
    token    = os.getenv("TOKEN")

    print("MY_USERNAME:", username)
    print("TOKEN:", token)

    # check that username is not None
    if username is None:
        raise ValueError("Username not set in .env file")
    
    # retrieve a list of your starred repositories
    repositories = get_starred_repositories(username, token)

    # search for issues with specified labels in each repository
    labels = 'good first issue,help wanted'
    issue_titles = get_issues_with_labels(repositories, labels, token)

    return issue_titles

def get_starred_repositories(username, token):
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
    repo_info = requests.get(f'https://api.github.com/repos/{repo_name}', headers={"Authorization": f"token {token}"}, timeout=10).json()
    return repo_info.get('archived', False)

def get_issues_for_label(repo_name, label, token):
    response = requests.get(f'https://api.github.com/repos/{repo_name}/issues', 
                            headers={"Authorization": f"token {token}"},
                            params={'state': 'open', 'labels': label}, timeout=10)
    issues = response.json()
    return issues

def get_open_issues(issues):
    return [issue for issue in issues if not re.search(r'fixed|fixed_in_dev', ', '.join(label['name'] for label in issue['labels']))]

def get_issues_with_labels(repositories, labels, token):
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