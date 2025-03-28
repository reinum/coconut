# possibly make this into an exe later
import requests
import subprocess
import multiprocessing
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()


owner = "reinum"
repo = "osu-cheating-speedrun"

# please dont steal kocur :(
ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

def get_default_branch(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Authorization": f"token {ACCESS_TOKEN}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("default_branch")
    else:
        print(f"Error: {response.status_code}, {response.json().get('message')}")
        return None

def get_latest_commit(owner, repo):
    branch = get_default_branch(owner, repo)
    if not branch:
        return None

    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{branch}"
    headers = {"Authorization": f"token {ACCESS_TOKEN}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commit = response.json()
        return commit["sha"][0:7], commit["commit"]["message"].split("\n\n")[0]
    else:
        print(f"Error: {response.status_code}, {response.json().get('message')}")
        return None

def pull_latest_commit(repo):
    r = subprocess.run(["git", "-C", "./"+repo, "pull"], capture_output=True, text=True)
    if r.returncode == 0:
        # install new dependencies if any
        r = subprocess.run(["pip", "install", "-r", "./"+repo+"/requirements.txt"], capture_output=True, text=True)
        if r.returncode == 0:
            return True
        else:
            raise Exception(r.stderr)
    else:
        raise Exception(r.stderr)
    
def watchdog(repo):
    if ".." in repo:
        print("Invalid repo name")
        return
    command = ["./bin/python3", "-u", f"./{repo}/main.py"]
    print(f"Running command: {' '.join(command)}")
    
    # Start the process
    process = subprocess.Popen(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True,
    text=True,
    env={"PYTHONUNBUFFERED": "1"}
    )
    
    print(f"Monitoring {repo}...")
    
    # Read and print the output line by line
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())

process = multiprocessing.Process(target=watchdog, args=(repo,))
process.start()
current_commit, _ = get_latest_commit(owner, repo)
# run file
print("checking for updates...")
while True:
    latest_commit = get_latest_commit(owner, repo)
    if latest_commit:
        latest_commit_hash, latest_commit_message = latest_commit
        # print(f"Latest commit: {latest_commit_hash} - {latest_commit_message}")
        if latest_commit_hash != current_commit:
            print(f"New commit detected: {latest_commit_hash} - {latest_commit_message}")
            try:
                pull_latest_commit(repo)
                print("Update successful!")
                current_commit = latest_commit_hash
                if process.is_alive():
                    process.terminate()
                    process.join()

                # Create a new process instance and start it
                process = multiprocessing.Process(target=watchdog, args=(repo,))
                process.start()
                print("Restarted process.")
            except Exception as e:
                print(f"Update failed: {e}")
        else:
            # print("No new commits")
            pass
    else:
        print("Error getting latest commit")