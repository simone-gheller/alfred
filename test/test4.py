# import sys
# from os import path
# sys.path.append(path.abspath(path.join(path.dirname(__file__), "..")))
from alfred.api.alfred import Step, Pipeline, run_pipeline
from alfred.api.git import clone
from alfred.api.steps import RetryStep, InteractiveStep

def checkout():
    return clone(repo_url='https://github.com/simone-gheller/blango.git',
                    destination_dir='blaghelito/blango1', 
                    branch='master')
    
def fail():
    raise RuntimeError('failing step')

def interactive():
    print('crucial task')

PIPELINE = Pipeline([
    Step(checkout),
    InteractiveStep(interactive),
    RetryStep(fail)
])

if __name__ == '__main__':
    result = run_pipeline()
    print(result)
