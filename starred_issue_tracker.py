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

        # search for issues with the "help-wanted" label in each repository
        issue_titles = []
        for repo_name in repositories:
        
            response = requests.get(f'https://api.github.com/repos/{repo_name}/issues', 
                                    headers=headers,
                                    params={'state': 'open', 'labels': 'bug'})
            issues = response.json()
            if issues:
                print(f"Repository '{repo_name}' has {len(issues)} open issues labeled 'bug'")
            else:
                print(f"Repository '{repo_name}' does not have any open issues labeled 'bug'")
                
                print(repo_name)

        return issue_titles
    
    except requests.exceptions.RequestException as e:
        print("Error retrieving issues:", e)
        return []

get_help_wanted_issues()