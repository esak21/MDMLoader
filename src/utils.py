import yaml

def read_configs(file_path: str):
    with open(file_path, 'r') as file:
        configs = yaml.safe_load(file)
    return configs



if __name__ == "__main__":
    file_name = "/Users/esak/Documents/Esakki/code_base/current_project/esak_edm_file_loader/configs.yaml"
    response = read_configs(file_name)
    print(response)