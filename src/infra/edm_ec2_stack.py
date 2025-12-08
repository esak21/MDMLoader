from aws_cdk import (
    aws_ec2 as _ec2,
    Stack, CfnOutput
)
from constructs import Construct
from src.infra.my_stack_props import Ec2StackProps

class Ec2Stack(Stack):
    """ A Stack That Deploys the Ec2 Instance """


    def __init__(self, scope:Construct, id: str , props: Ec2StackProps, **kwargs) -> None :
        super().__init__(scope, id, **kwargs)

        edm_vpc  = _ec2.Vpc.from_lookup(
            self,
            "DefaultVPC",
            is_default=True
        )

        edm_instance = _ec2.Instance(self,
                      "EDM-EC2-Instance",
                      instance_type = _ec2.InstanceType(props.instance_type),
                      machine_image = _ec2.MachineImage.latest_amazon_linux2023(),
                      vpc = edm_vpc

                      )

        CfnOutput(self, "InstanceId", value=edm_instance.instance_id)
        print(f"newly Created Instances are : {edm_instance.instance_id}")


