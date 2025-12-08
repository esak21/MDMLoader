import yaml

def read_configs(file_path: str):
    with open(file_path, 'r') as file:
        configs = yaml.safe_load(file)
    return configs



if __name__ == "__main__":
    file_name = "/configs.yaml"
    response = read_configs(file_name)
    print(response)