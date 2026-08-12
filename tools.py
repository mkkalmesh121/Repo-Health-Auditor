import requests

def get_repo_metadata(repo_url):
    repo = repo_url.replace("https://github.com/", "")
    api = f"https://api.github.com/repos/{repo}"

    response = requests.get(api)

    if response.status_code != 200:
        return {"error": "Repository not found"}

    data = response.json()

    return {
        "name": data["name"],
        "owner": data["owner"]["login"],
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "issues": data["open_issues_count"],
        "language": data["language"],
        "license": data["license"]["name"] if data["license"] else "None",
        "updated": data["updated_at"]
    }