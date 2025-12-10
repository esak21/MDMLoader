import os

from aws_cdk import (
    Stack,
aws_ec2 as _ec2
)
from constructs import Construct
from src.gears import *
from src.gears.fargate_gear import FargateGear
from src.gears.sns_gear import SNSGear
from src.gears.s3_gear import S3gear
from src.gears.lambda_gear import LambdaGear
from src.infra.my_stack_props import SNSGearprops

from src.config_parser import get_gear_props

class AppStack(Stack):
    """
    A stack that deploys an S3 bucket.
    """
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id,  **kwargs)
        self.deploy_env =  os.environ.get("env")

        default_vpc = _ec2.Vpc.from_lookup(
            self,
            "DefaultVpcLookup",
            is_default=True
        )

        print(f"we are going to build the app in teh VPC  {default_vpc}")


        sns_gear_props = get_gear_props("sns", self.deploy_env)
        print(sns_gear_props)
        app_sns = SNSGear(self, "EDM-APP-SNS-Topic", props=sns_gear_props)
        print(app_sns.to_string)
        s3_gear_props = get_gear_props("s3", self.deploy_env)
        app_bucket = S3gear(self,"EDM-APP-S3-Bucket", props=s3_gear_props)


        batch_gear_props = get_gear_props("batch", self.deploy_env)
        app_batch = FargateGear(self,"EDM-APP-BATCH", props=batch_gear_props)

        lambda_gear_props = get_gear_props("lambda", self.deploy_env)
        app_lambda = LambdaGear(self,"EDM-APP-LAMBDA", props=lambda_gear_props)

        print("My App Stack is created")
        app_lambda.node.add_dependency(app_sns)
        app_batch.node.add_dependency(app_lambda)
        app_bucket.node.add_dependency(app_lambda)







