def read_input(file,sep: str = '\n'):
    with open(file, "r") as tf:        
        return tf.read().strip().split(sep)

def flatten(t):
    return [item for sublist in t for item in sublist]