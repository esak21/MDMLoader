import aws_cdk as cdk
from src.lib.edm_stage import EDMAppStage
from src.lib.utils import read_configs
import os

app = cdk.App()

accounts_info = read_configs("/Users/esak/Documents/Esakki/code_base/current_project/esak_edm_file_loader/src/configs/accounts.yaml")
env = os.environ.get("env")
print(accounts_info)
print(env)
account_id = accounts_info.get(env).get("account")
region = accounts_info.get(env).get("region")

EDMAppStage(app, 'EDM-QA',
           env=cdk.Environment(account='905418448077', region='us-east-1'),
           )

app.synth()

