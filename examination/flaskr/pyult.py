import os

def generate_abspath(base_file, dest_file):
    path = os.path.dirname(base_file)
    path = os.path.join(path, dest_file)
    abspath = os.path.abspath(path)
    return abspath