import os

def read_input(file,sep: str = '\n'):
    with open(file, "r") as tf:        
        return tf.read().strip().split(sep)

def flatten(t):
    return [item for sublist in t for item in sublist]

def get_txt_files(current_script_path):
    data_paths = {}
    # Get the path of the current script file    
    current_dir = os.path.dirname(current_script_path)    
    # For each .txt file in the current directory and its subdirectories
    for root, _, files in os.walk(current_dir):
        for file in files:
            if file.endswith('.txt'):
                data_type = file.split('.')[0]
                data_paths[data_type] = os.path.join(root, file)
    return data_paths