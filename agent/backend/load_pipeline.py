import importlib.util
import sys

def load_pipeline(file_path):
    spec = importlib.util.spec_from_file_location("user_pipeline", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.PIPELINE