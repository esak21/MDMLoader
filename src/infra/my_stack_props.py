from aws_cdk import StackProps

class s3StackProps(StackProps):
    """
    Props for the EC2Stack.
    """
    def __init__(self, bucket_name: str, **kwargs):
        super().__init__(**kwargs)
        self.bucket_name = bucket_name


class Ec2StackProps(StackProps):
    def __init__(self, instance_type: str, ami_id: str, **kwargs):
        super().__init__(**kwargs)
        self.instance_type = instance_type
        self.ami_id = ami_id

