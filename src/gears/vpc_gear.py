from constructs import Construct
from aws_cdk import (
    aws_ec2 as _ec2
)

class network(Construct):
    def __init__(self, scope: Construct , construct_id: str , **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        default_vpc = _ec2.Vpc.from_lookup(
            self,
            "DefaultVpcLookup",
            is_default=True
        )