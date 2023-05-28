import yaml

def load_TOSCA(path):
    with open(path, 'r') as stream:
            data = yaml.safe_load(stream)
            return data