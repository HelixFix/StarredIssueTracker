import re
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
username = os.getenv("MY_USERNAME")
token    = os.getenv("TOKEN")


header       = {"Authorization": f"token {token}"}
labels       = 'help-wanted,contributions-welcome,good-first-issue,hacktoberfest,beginner-friendly,good-first-bug,easy,low-hanging-fruit,first-timers-only,good first issue,help wanted'
label_list   = labels.split(',')
issue_titles = []


def get_help_wanted_issues():
    
    print("MY_USERNAME:", username)
    print("TOKEN:", token)

    if username is None:
        raise ValueError("Username not set in .env file")
    
    issue_titles.clear()

    for repo_name in get_repositories(username, header):
        open_issues     = get_open_issues(repo_name, header, label_list)
        relevant_issues = filter_relevant_issues(open_issues)
        issues          = [issue['title'] for issue in relevant_issues]
        issue_titles.extend(issues)

    #return issue_titles


def get_repositories(username, header):
    url = f"https://api.github.com/users/{username}/starred"
    response = requests.get(url, headers=header)
    response.raise_for_status()
    repositories = [repo["full_name"] for repo in response.json()]
    return repositories


def get_open_issues(repo_name, header, labels):
    issues = []
    for label in labels:
        url      = f'https://api.github.com/repos/{repo_name}/issues'
        params   = {'state': 'open', 'labels': label}
        response = requests.get(url, headers=header, params=params)
        issues.extend(response.json())
        if issues:
            print(f"Repository '{repo_name}' (https://github.com/{repo_name}) has {len([issue for issue in issues if not re.search(r'fixed|fixed_in_dev', ', '.join(label['name'] for label in issue['labels']))])} open issues labeled '{label}'")
            for issue in issues:
                issue_titles.append(issue['title'])
        #else:
           # print(f"Skipping archived repository '{repo_name}'")
    return issues


def filter_relevant_issues(issues):
    relevant_issues = []
    for issue in issues:
        labels = [label['name'] for label in issue['labels']]
        if not any(label in labels for label in ['fixed', 'fixed_in_dev']):
            relevant_issues.append(issue)
    return relevant_issues


issue_titles = get_help_wanted_issues()
print(issue_titles)
