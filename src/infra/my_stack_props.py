from aws_cdk import StackProps

class s3StackProps(StackProps):
    """
    Props for the EC2Stack.
    """
    def __init__(self, bucket_name: str, **kwargs):
        super().__init__(**kwargs)
        self.bucket_name = bucket_name

class S3Gearprops(StackProps):
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

class SNSGearprops:
    def __init__(self, topic_name: str, email: str  ):
        self.topic_name = topic_name
        self.email = email


class BATCHGearprops:
    def __init__(self, platform : str, job_queue_name: str, priority: int, enabled: bool, compute_environment_order: dict, existing_batch_tasks_role_arn: str, existing_batch_tasks_execution_role_arn: str):
        self.platform = platform
        self.job_queue_name = job_queue_name
        self.priority = priority
        self.enabled = enabled
        self.compute_environment_order = compute_environment_order
        self.existing_batch_tasks_role_arn = existing_batch_tasks_role_arn
        self.existing_batch_tasks_execution_role_arn = existing_batch_tasks_execution_role_arn


class LambdaGearprops:
    def __init__(self, function_name: str, runtime: str, code: str, handler: str, role_arn: str):
        self.function_name = function_name
        self.runtime = runtime
        self.code = code
        self.handler = handler
        self.role_arn = role_arn