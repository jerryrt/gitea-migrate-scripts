import requests
import time
import json
import os
from requests.adapters import HTTPAdapter

# Debug mode toggle
DEBUG = True

# Gitea configuration (Token authentication only)
# Import from environment variables
GITEA_URL = os.getenv('GITEA_URL', 'http://localhost:3000')
GITEA_USERNAME = os.getenv('GITEA_USERNAME', 'nobody')
GITEA_PASSWORD = os.getenv('GITEA_PASSWORD', 'password')
GITEA_TOKEN = os.getenv('GITEA_TOKEN', 'token')
GITEA_ORG = os.getenv('GITEA_ORG', 'gitea_org')

# GitHub configuration (Token authentication only)
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME', 'nobody')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', 'token')
GITHUB_ORG = os.getenv('GITHUB_ORG', 'github_org')

def debug_log(message):
    """Print debug messages only when DEBUG mode is enabled."""
    if DEBUG:
        print("[DEBUG]", message)

RESULT_JSON = 'finishedRepoOrg.json'
def load_finished_repos(file_path=RESULT_JSON):
    """
    Load the list of finished repositories.
    If the file does not exist or the data format is invalid, return an empty list.
    """
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    debug_log(f"Data in {RESULT_JSON} is not a list, resetting to an empty list.")
                    return []
                return data
        except json.JSONDecodeError:
            debug_log(f"{RESULT_JSON} format error, resetting to an empty list.")
            return []
    return []

def save_finished_repos(data, file_path=RESULT_JSON):
    """
    Save the list of finished repositories to a file.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Load finished repository records
finishedRepo = load_finished_repos()

def fetch_github_repos(page, per_page=100):
    """
    Fetch the list of repositories from GitHub for the specified page.
    Args:
        page (int): Page number.
        per_page (int): Number of repositories per page (default is 100).
    Returns:
        list: A list of repositories, or an empty list if the request fails.
    """
    url = f"https://api.github.com/orgs/{GITHUB_ORG}/repos?per_page={per_page}&page={page}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        repos = response.json()
        debug_log(f"Fetched GitHub repositories page {page}, count: {len(repos)}")
        return repos
    except requests.RequestException as e:
        debug_log(f"Failed to fetch GitHub repositories (page {page}): {e}")
        return []

def migrate_repo(repo):
    """
    Migrate a single GitHub repository to Gitea.
    Args:
        repo (dict): GitHub repository information.
        uid (int): Gitea user ID.
    """
    repo_clone_url = repo.get('clone_url')
    repo_name = repo.get('name')
    description = repo.get('description') or ""
    
    print(f"Starting migration of repository: {repo_name}")
    print(f"Clone URL: {repo_clone_url}")
    
    # Replace the GitHub domain in the clone URL and add authentication info
    clone_addr = repo_clone_url.replace(
        "https://github.com",
        f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com"
    )
    
    session = requests.Session()
    session.mount("http://", HTTPAdapter(max_retries=3))
    session.mount("https://", HTTPAdapter(max_retries=3))
    
    # Only include necessary parameters, remove unnecessary ones
    payload = {
        'clone_addr': clone_addr,
        'mirror': False,
        'private': True,
        'repo_name': repo_name,
        'repo_owner': GITEA_ORG,
        'description': description
    }
    debug_log(f"Migration payload: {payload}")
    
    try:
        response = session.post(
            f"{GITEA_URL}/api/v1/repos/migrate",
            json=payload,
            auth=(GITEA_USERNAME, GITEA_PASSWORD),
            timeout=120
        )
        debug_log(f"Response status code: {response.status_code}")
        response_data = response.json()
        debug_log(f"Response data: {response_data}")
        
        if response.status_code == 409 or response_data.get('id', 0) > 0:
            finishedRepo.append({
                'name': repo_name,
                'clone_addr': repo_clone_url,
                'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                'created': response.status_code != 409
            })
            save_finished_repos(finishedRepo)
            
            if response.status_code == 409:
                print(f"{repo_name}: Repository already exists.")
            else:
                print(f"{repo_name}: Repository migrated successfully!")
        else:
            print(f"{repo_name}: Migration failed!")
            print(response_data)
    except Exception as e:
        print(f"{repo_name}: Request exception - {e}")

def migrate_all_repos():
    """
    Fetch GitHub repositories page by page and migrate them one by one.
    Args:
        uid (int): Gitea user ID.
    """
    page = 1
    while True:
        repos = fetch_github_repos(page)
        if not repos:
            print("No more repositories, migration ended.")
            break
        
        for repo in repos:
            # Skip if the repository is already in finishedRepo
            if any(item.get('name') == repo.get('name') for item in finishedRepo):
                print(f"{repo.get('name')}: Already completed, skipping.")
                continue
            
            print(f"Starting migration of repository: {repo}")
            migrate_repo(repo)
            # Delay to avoid too frequent requests
            time.sleep(30)
        page += 1

if __name__ == '__main__':
    print("Starting Gitea repository migration program")
    
    migrate_all_repos()
    print("All repository migrations have been processed.")
