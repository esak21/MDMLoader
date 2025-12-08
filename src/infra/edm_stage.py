from aws_cdk import Stage
from constructs import Construct
import os
from src.infra.utils import read_configs
from src.infra.edm_s3_stacks import  S3Stack
from src.infra.edm_ec2_stack import Ec2Stack
from src.infra.my_stack_props import s3StackProps, Ec2StackProps
from pathlib import Path

env = os.environ.get("env")
print(Path.cwd())
configs = read_configs(f"/Users/esak/Documents/Esakki/code_base/current_project/esak_edm_file_loader/src/configs/{env}.yaml")
print(configs)

# Define the stage
class EDMAppStage(Stage):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Add both stacks to the stage
        storage_props = s3StackProps(
            bucket_name=configs.get("bucket_name"),
        )

        ec2_props = Ec2StackProps(
            instance_type=configs.get("instance_type"),
            ami_id=configs.get("ami_id")
        )

        edm_storage_stack = S3Stack(self, "edm-app-infra-storage", props=storage_props)
        edm_compute_stack = Ec2Stack(self, "edm-app-infra-compute", props=ec2_props)

        edm_compute_stack.add_dependency(edm_storage_stack)

