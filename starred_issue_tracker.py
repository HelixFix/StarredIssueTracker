import re
import requests
from dotenv import load_dotenv
import os
import json

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
    url      = f"https://api.github.com/users/{username}/starred"
    headers  = {"Authorization": f"token {token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        repositories = [repo["full_name"] for repo in response.json()]

        # search for issues with specified labels in each repository
        labels = 'help-wanted,contributions-welcome,good-first-issue,hacktoberfest,beginner-friendly,good-first-bug,easy,low-hanging-fruit,first-timers-only,bug'
        label_list = labels.split(',') # split string into list of labels
        issue_titles = []
        for repo_name in repositories:
            for label in label_list: # iterate over labels
                response = requests.get(f'https://api.github.com/repos/{repo_name}/issues', 
                                        headers=headers,
                                        params={'state': 'open', 'labels': label})
                issues = response.json()
                if issues:
                    print(f"Repository '{repo_name}' (https://github.com/{repo_name}) has {len([issue for issue in issues if not re.search(r'fixed|fixed_in_dev', ', '.join(label['name'] for label in issue['labels']))])} open issues labeled '{label}'")
                    for issue in issues:
                        issue_titles.append(issue['title'])
                #else:
                 #   print(f"Repository '{repo_name}' does not have any open issues labeled '{label}'")
                    
                 #   print(repo_name)

        return issue_titles
    
    except requests.exceptions.RequestException as e:
        print("Error retrieving issues:", e)
        return []

get_help_wanted_issues()