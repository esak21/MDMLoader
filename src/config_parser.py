import yaml

from src.infra.my_stack_props import *


def get_model_name(gear_name: str ):
    return {
        "SNS" : SNSGearprops,
        "S3" : S3Gearprops,
        "BATCH" : BATCHGearprops,
        "LAMBDA" : LambdaGearprops
    }


def read_configs(file_path: str):
    with open(file_path, 'r') as file:
        configs = yaml.safe_load(file)
    return configs

def get_gear_props(gear_name:str, env: str ):
    configs = read_configs(f"/Users/esak/Documents/Esakki/code_base/current_project/esak_edm_file_loader/src/configs/{env}.yaml")
    print(configs.get(gear_name.upper()))
    if configs.get(gear_name.upper()):
        print(f"Gear Information is available in the config File {configs.get(gear_name.upper())}")
        required_param: dict = configs.get(gear_name.upper())
        model = get_model_name(gear_name)[gear_name.upper()]
        gear_props = model(**required_param)
        print(gear_props)
        return gear_props
    else:
        print(f"Gear Information is NOT available in the config File {configs.get(gear_name.upper())}")
        return None


if __name__ == "__main__":
    # file_name = "/Users/esak/Documents/Esakki/code_base/current_project/esak_edm_file_loader/configs.yaml"
    # response = read_configs(file_name)
    # print(response)
    print(get_gear_props("s3", "qa"))

