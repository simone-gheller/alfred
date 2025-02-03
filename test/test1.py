# import sys
# from os import path
# sys.path.append(path.abspath(path.join(path.dirname(__file__), "..")))
from alfred.api.alfred import Step, Pipeline, run_pipeline
from alfred.api.shell import Shell

def step1():
    return "hello world"

def step2(data):
    return data.upper()

def step_e():
    import time
    time.sleep(10)

def step_script():
    from os import path
    s = path.abspath(path.join(path.dirname(__file__), "script1.sh"))
    c = Shell.run_script(s, output=True)
    print(c)
    

PIPELINE = Pipeline([
    Step(step1),
    Step(step2),
    Step(step_script),
    Step(step_e)
])

if __name__ == '__main__':
    result = run_pipeline()
    print(result)
