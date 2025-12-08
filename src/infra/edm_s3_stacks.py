from aws_cdk import (
    Stack,
    aws_s3 as _s3
)
from typing import Optional
from constructs import Construct

from App_stacks.MyS3props import s3StackProps


class S3Stack(Stack):
    """
    A stack that deploys an S3 bucket.
    """
    def __init__(self, scope: Construct, id: str, props: Optional[s3StackProps] = None, **kwargs) -> None:
        super().__init__(scope, id,  **kwargs)


        edm_bucket = _s3.Bucket(
            self,
            "EDM-APP-Bucket_id",
            bucket_name=props.bucket_name,
            versioned=True,
        )

        bucket_arn = edm_bucket.bucket_arn
        print(f"The ARN of the bucket is: {bucket_arn}")

