import sys
import os
import requests
import hashlib
import shutil
import base64
import time

def get_headers(token=None):
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    return headers

def get_latest_commit_sha(owner, repo, branch='main', token=None):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits/{branch}'
    response = requests.get(url, headers=get_headers(token))
    response.raise_for_status()
    data = response.json()
    return data['sha']

def get_tree_sha_from_commit(owner, repo, commit_sha, token=None):
    url = f'https://api.github.com/repos/{owner}/{repo}/git/commits/{commit_sha}'
    response = requests.get(url, headers=get_headers(token))
    response.raise_for_status()
    data = response.json()
    return data['tree']['sha']

def get_tree_recursive(owner, repo, tree_sha, token=None):
    url = f'https://api.github.com/repos/{owner}/{repo}/git/trees/{tree_sha}?recursive=1'
    response = requests.get(url, headers=get_headers(token))
    response.raise_for_status()
    data = response.json()
    return data['tree']

def get_blob_content(owner, repo, sha, token=None):
    url = f'https://api.github.com/repos/{owner}/{repo}/git/blobs/{sha}'
    response = requests.get(url, headers=get_headers(token))
    response.raise_for_status()
    data = response.json()
    content = data['content']
    encoding = data['encoding']
    if encoding == 'base64':
        content_bytes = base64.b64decode(content)
        return content_bytes
    else:
        raise ValueError(f"Unknown encoding: {encoding}")

def get_remote_C_files(owner, repo, branch='main', token=None):
    latest_commit_sha = get_latest_commit_sha(owner, repo, branch, token)
    latest_tree_sha = get_tree_sha_from_commit(owner, repo, latest_commit_sha, token)
    tree = get_tree_recursive(owner, repo, latest_tree_sha, token)
    remote_files = {}
    for item in tree:
        if item['type'] == 'blob' and item['path'].startswith('C/'):
            remote_files[item['path']] = item['sha']
    return remote_files

def get_local_C_files_hashes(base_path):
    local_files = {}
    C_path = os.path.join(base_path, 'C')
    if not os.path.exists(C_path):
        return local_files
    for root, dirs, files in os.walk(C_path):
        for name in files:
            filepath = os.path.join(root, name)
            relative_path = os.path.relpath(filepath, base_path).replace('\\', '/')
            with open(filepath, 'rb') as f:
                content = f.read()
            sha1 = hashlib.sha1(content).hexdigest()
            local_files[relative_path] = sha1
    return local_files

def is_C_folder_up_to_date(owner, repo, branch='main', token=None, base_path='.'):
    # Check if it's been less than an hour since the last check
    cache_file = os.path.join(base_path, '.last_check_time')
    current_time = time.time()
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            last_check_time = float(f.read())
        if current_time - last_check_time < 3600:  # 3600 seconds = 1 hour
            print("Last check was less than an hour ago. Skipping update check.")
            return True  # Assume up-to-date to skip API calls
    # Proceed with the update check
    remote_files = get_remote_C_files(owner, repo, branch, token)
    local_files = get_local_C_files_hashes(base_path)
    if set(remote_files.keys()) != set(local_files.keys()):
        return False
    for path in remote_files:
        remote_sha = remote_files[path]
        local_sha = local_files.get(path)
        if local_sha is None:
            return False
        remote_content = get_blob_content(owner, repo, remote_sha, token)
        remote_content_sha1 = hashlib.sha1(remote_content).hexdigest()
        if remote_content_sha1 != local_sha:
            return False
    # Update the last check time
    with open(cache_file, 'w') as f:
        f.write(str(current_time))
    return True

def download_C_folder(owner, repo, branch='main', token=None, base_path='.'):
    remote_files = get_remote_C_files(owner, repo, branch, token)
    C_path = os.path.join(base_path, 'C')
    if os.path.exists(C_path):
        shutil.rmtree(C_path)
    for path, sha in remote_files.items():
        content = get_blob_content(owner, repo, sha, token)
        local_path = os.path.join(base_path, path.replace('/', os.sep))  # Convert to OS-specific path
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'wb') as f:
            f.write(content)

def main():
    owner = 'GeneralLPrince'
    repo = 'checkuit'
    branch = 'main'
    token = None  # Or use os.getenv('GITHUB_TOKEN') if you have a token
    base_path = '/workspaces/checkuit'

    try:
        if not is_C_folder_up_to_date(owner, repo, branch, token, base_path):
            print("checkuit n'est pas à jour. Téléchargement de la dernière version...")
            download_C_folder(owner, repo, branch, token, base_path)
            print("checkuit est à jour.")
        else:
            print("checkuit est déjà à jour.")
    except Exception as e:
        pass

    current_path = os.path.dirname(os.path.abspath(__file__))

    def run_python_file(file_path):
        context = {
            'codePath': [file_path, os.getcwd()],
        }
        with open(file_path, 'r') as file:
            code = file.read()
            exec(code, {}, context)

    if len(sys.argv) > 1:
        script_to_run = os.path.join(current_path, sys.argv[1])
        run_python_file(script_to_run)
    else:
        print("Veuillez fournir le chemin du fichier test.")

if __name__ == '__main__':
    main()

#checkuit/C/IA/2024/Structures/Exercice1/test_python.py
