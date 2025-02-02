import os
from api.alfred import Pipeline

def set_working_directory(directory: str):
    if not os.path.exists(directory):
        raise ValueError(f"Invalid folder name")
    os.chdir(directory)

def archive_artifact(path: str, copy: bool = False):
    if not os.path.exists(path):
        raise ValueError(f"Invalid path")
    dest_dir = os.path.join(Pipeline.work_dir, 'artifacts')
    Pipeline.archive[os.path.basename(path)] = os.path.abspath(path)
    if copy:
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir) 
        dest = os.path.join(dest_dir, os.path.basename(path))
        import shutil
        shutil.copy(path, dest)

def get_artifact(artifact: str):
    return Pipeline.archive.get(artifact, None)

def interactive_choice(msg: str):
    options = ['Continue', 'Abort']
    msg = msg if msg is not None else f"Please select an option (1-{len(options)}): "
    choice = input(msg)
    if choice.isdigit() and 1 <= int(choice) <= len(options):
        print(f"You selected: {options[int(choice)-1]}")
    else:
        print("Invalid selection, using default behavior.")
    