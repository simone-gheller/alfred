# test/test2.py
from alfred.api.alfred import Step, run_pipeline, Pipeline
from alfred.api.steps import OnFailure
from alfred.api.git import clone
from alfred.api.shell import Shell
from alfred.api.utils import set_working_directory

def checkout():
    return clone(repo_url='https://github.com/simone-gheller/blango.git',
                    destination_dir='blaghelito/blango2', 
                    branch='master')
    
def cd_print(path):
    set_working_directory(path)
    Shell.run("pwd")

def fail():
    raise Exception('ewkjfn')

def get_insight():
    Shell.run("echo suca")

# Inizializzazione globale
Pipeline([
    Step(checkout),
    Step(cd_print),
    OnFailure(get_insight)
])

if __name__ == '__main__':
    result = run_pipeline()
    print(result)
