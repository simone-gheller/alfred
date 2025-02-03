# import sys
# from os import path
# sys.path.append(path.abspath(path.join(path.dirname(__file__), "..")))
from alfred.api.alfred import Step, Pipeline, run_pipeline
from alfred.api.git import clone
from alfred.api.shell import Shell
from alfred.api.utils import set_working_directory, archive_artifact, get_artifact

def checkout():
    return clone(repo_url='https://github.com/simone-gheller/blango.git',
                    destination_dir='blaghelito/blango4', 
                    branch='master')
    
def archive(repo):
    set_working_directory(repo)
    archive_artifact("README.md")

def get_arti():
    artifact = get_artifact("README.md")
    with open(artifact) as f:
        print(f.read())

PIPELINE = Pipeline([
    Step(checkout),
    Step(archive),
    Step(get_arti)
])

if __name__ == '__main__':
    result = run_pipeline()
    print(result)
