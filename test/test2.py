# import sys
# from os import path
# sys.path.append(path.abspath(path.join(path.dirname(__file__), "..")))
from api.alfred import Step, Pipeline, run_pipeline
from api.steps import OnFailure
from api.git import clone
from api.shell import Shell
from api.utils import set_working_directory

def checkout():
    return clone(repo_url='https://github.com/simone-gheller/blango.git',
                    destination_dir='blaghelito/blango3', 
                    branch='master')
    
def cd_print(path):
    set_working_directory(path)
    Shell.run("pwd")

def fail():
    raise Exception('ewkjfn')

def get_insight():
    Shell.run("echo suca")

PIPELINE = Pipeline([
    Step(checkout),
    Step(cd_print),
    # Step("fail", fail),
    OnFailure(get_insight)
])

if __name__ == '__main__':
    result = run_pipeline()
    print(result)
