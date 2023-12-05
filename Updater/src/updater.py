from flask import Flask, request
import subprocess
import json  # Import the json module
import requests

app = Flask(__name__)

def update_commit_status(workspace, repo_slug, commit_id, state, description, access_token):
    url = f"https://bitbucket.example.com/rest/build-status/1.0/commits/{commit_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "state": state,
        "description": description,
        "key": description,
        "logs": description,
        "url": "https://example.com"  # URL to more details or logs
    }
     
    response = requests.post(url, headers=headers, json=data)
    return response.status_code

@app.route('/update', methods=['GET','POST'])
def webhook():
    if request.method == 'POST':
        # Parse the JSON payload
        payload = json.loads(request.data)
        
        # Extract workspace and repo_slug from the payload
        workspace = payload['repository']['project']['key']
        repo_slug = payload['repository']['slug']
        # Replace with your actual access token
        access_token = "yoru bitbucket api token"

        if request.headers.get('X-Event-Key') == 'diagnostics:ping':
            return 'Ping test received', 200
        # Example: Check for a specific event  
        
        if payload.get('eventKey') == 'repo:refs_changed':
            for change in payload['changes']:
                if change['ref']['id'] == "refs/heads/master":
                    commit_id = change['toHash']  # Get the commit displayId
                    subprocess.call(['git', '-C', '/root/repo', 'pull'])
                    update_commit_status(workspace,repo_slug,commit_id, "SUCCESSFUL", f'Update executed on master branch for commit {commit_id}', access_token)
                    return f'Git pull executed on master branch for commit {commit_id}', 200

        # Check for a pull request merged into the master branch
        
        elif payload.get('eventKey') == 'pr:merged':
            if payload['pullRequest']['toRef']['id'] == "refs/heads/master":
                commit_id = payload['pullRequest']['toRef']['latestCommit']  # Get the commit displayId
                subprocess.call(['git', '-C', '/root/repo', 'pull'])
                update_commit_status(commit_id, "SUCCESSFUL", f'Update executed for merged pull request into master for commit {commit_id}', access_token)
                return f'Git pull executed for merged pull request into master for commit {commit_id}', 200
        else:
            return 'Ignored event', 200
    if request.method == 'GET':
        subprocess.call(['git', '-C', '/root/repo', 'pull'])
        return 'Success', 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

