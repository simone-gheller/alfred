from git import Repo
import os
from api.alfred import Pipeline

def clone(repo_url, destination_dir=None, branch=None):
    if not destination_dir:
        destination_dir = repo_url.split("/")[-1].replace(".git", "")
    print(f"Cloning into 'f{destination_dir}'...")
    prefix = Pipeline.work_dir
    repo = Repo.clone_from(repo_url, os.path.join(prefix, destination_dir), branch=branch)
    print("Repository cloned successfully!")
    return repo.working_dir