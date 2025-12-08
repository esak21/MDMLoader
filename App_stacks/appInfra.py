from constructs import Construct
from aws_cdk import (
    Stack,
    StackProps,
    CfnOutput,
    aws_ec2 as ec2,
    aws_s3 as _s3,

)
from typing import Optional, TypedDict
import yaml
from pathlib import Path
import os
import sys


class MyCustomStackProps(StackProps):
    """
    Custom properties for MyCustomStack.
    """
    def __init__(self, *, bucket_name: str, enable_versioning: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.bucket_name = bucket_name
        self.enable_versioning = enable_versioning

# --- 2. Create the Stack using the Custom Props Class ---
class MyConfigurableStack(Stack):
    # FIX: Make props optional to avoid the TypeError and use **kwargs to capture all inputs
    def __init__(self, scope: Construct, construct_id: str,  props: MyCustomStackProps,
                 **kwargs) -> None:

        # Pass standard StackProps up to the parent constructor
        super().__init__(scope, construct_id, **kwargs)

        # Safely extract configuration from either the props object or the **kwargs dictionary

        print(props)
        print(props.bucket_name)

        _s3.Bucket(
            self,
            "MyS3Bucket",
            bucket_name=props.bucket_name,
            versioned=props.enable_versioning,
        )