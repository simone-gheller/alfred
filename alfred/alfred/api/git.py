from git import Repo
import os

def clone(repo_url, destination_dir=None, branch=None):
    # from api.pipeline import PIPELINE

    if not destination_dir:
        destination_dir = repo_url.split("/")[-1].replace(".git", "")
    print(f"Cloning into '{destination_dir}'...")
    # prefix = PIPELINE.work_dir
    from alfred.api.alfred import Pipeline
    prefix = Pipeline.work_dir
    repo = Repo.clone_from(repo_url, os.path.join(prefix, destination_dir), branch=branch)
    print("Repository cloned successfully!")
    return repo.working_dir
