import aws_cdk as cdk
from src.AppStack import AppStack
from src.infra.utils import read_configs
import os

app = cdk.App()

accounts_info = read_configs("/Users/esak/Documents/Esakki/code_base/current_project/esak_edm_file_loader/src/configs/accounts.yaml")
env = os.environ.get("env")
print(accounts_info)
print(env)
account_id = accounts_info.get(env).get("account")
region = accounts_info.get(env).get("region")

target_env = cdk.Environment(account=account_id, region=region)

AppStack(app, "EDM-QA", env = target_env)

app.synth()

