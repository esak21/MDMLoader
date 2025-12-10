from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_iam as _iam,
    Size
)

from src.infra.my_stack_props import BATCHGearprops


class LambdaGear(Construct):

    def __init__(self, scope: Construct, id: str, props: BATCHGearprops, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Let's Create the IAm Roles
        existing_role_arn = "arn:aws:iam::905418448077:role/EsakkiLambdaRootRoles"
        existing_role = _iam.Role.from_role_arn(self, "EDM_INFRA_ROLE", existing_role_arn , mutable=False)



        # Lets create the EDM Lambda
        edm_lambda = _lambda.Function(self, "EDMLambda",
                                      function_name="EDM_APP_LAMBDA",
                                      runtime=_lambda.Runtime.PYTHON_3_11,
                                      code=_lambda.Code.from_asset("nextgenlambda"),
                                      handler="infraRunner.lambda_handler",
                                      role=existing_role
                                      )