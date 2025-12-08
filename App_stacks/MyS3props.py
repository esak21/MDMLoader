import aws_cdk as cdk

# Define custom StackProps for the EC2 stack
class s3StackProps(cdk.StackProps):
    """
    Props for the EC2Stack.
    """
    def __init__(self, bucket_name: str, **kwargs):
        super().__init__(**kwargs)
        self.bucket_name = bucket_name
