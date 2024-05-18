import yaml

def load_yaml(path):
    with open(path, 'r') as fi:
        return yaml.load(fi, yaml.CLoader)
