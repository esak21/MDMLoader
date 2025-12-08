from inspect import stack
from pathlib import Path
from typing import Optional

import yaml
from constructs import Construct

from aws_cdk import (
    aws_lambda as _lambda,
    Stack,
    StackProps,
    aws_iam as _iam,
    aws_batch as _batch,
    aws_ec2 as _ec2,
    aws_ecs as _ecs, Size

)




class AppInfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Look up the default VPC in the current region/account
        default_vpc = _ec2.Vpc.from_lookup(
            self,
            "DefaultVpcLookup",
            is_default=True
        )

        existing_batch_tasks_role_arn = "arn:aws:iam::905418448077:role/MyBatchJoBRoles"
        existing_batch_tasks_role = _iam.Role.from_role_arn(self, "EDM_BATCH-TASK-INFRA-ROLE", existing_batch_tasks_role_arn, mutable=False)
        existing_batch_tasks_execution_role_arn = "arn:aws:iam::905418448077:role/BatchEcsTaskExecutionRole"
        existing_batch_tasks_execution_role = _iam.Role.from_role_arn(self, "EDM_BATCH-TASK-INFRA-EXE-ROLE",
                                                            existing_batch_tasks_execution_role_arn, mutable=False)
        # Let's Create the IAm Roles
        existing_role_arn = "arn:aws:iam::905418448077:role/EsakkiLambdaRootRoles"
        existing_role = _iam.Role.from_role_arn(self, "EDM_INFRA_ROLE", existing_role_arn , mutable=False)

        existing_batch_service_role_arn = "arn:aws:iam::905418448077:role/aws-service-role/batch.amazonaws.com/AWSServiceRoleForBatch"
        existing_batch_service_role = _iam.Role.from_role_arn(self, "EDM_BATCH_INFRA_ROLE", existing_batch_service_role_arn , mutable=False)


        # Leta Create a BATCH Compute Environment
        fargate_compute_environment = _batch.FargateComputeEnvironment(
            self,
             "EDM-ANALYZER-PREMIUM",
            compute_environment_name= "EDM-ANALYZER-PREMIUM",
                maxv_cpus= 16 ,
            spot= True,
            vpc_subnets= _ec2.SubnetSelection(subnet_type=_ec2.SubnetType.PUBLIC),
            #security_group= _ec2.SecurityGroup.from_security_group_id(self, "EDM-ANALYZER-PREMIUM", 'sg-0ece7828869b52df5')
            vpc = default_vpc

        )

        job_queue = _batch.JobQueue(
            self,
            "EDM-ANALYZER-QUEUE",
            job_queue_name= "EDM-ANALYZER-QUEUE",
            priority= 10,
            enabled= True,
        )
        job_queue.add_compute_environment(compute_environment=fargate_compute_environment, order = 1 )

        # Create a Job Definition
        fargate_container_definition = _batch.EcsFargateContainerDefinition(
            self,
            "EDM-ANALYZER-JOB-DEFINITION",
            image = _ecs.ContainerImage.from_registry("905418448077.dkr.ecr.us-east-1.amazonaws.com/edm_app"),
            memory=Size.mebibytes(512),
            cpu = 0.25,
            job_role = existing_batch_tasks_role,
            execution_role= existing_batch_tasks_execution_role,
            command = ["python", "src/runner.py" , "gym_membership.csv"]


        )

        fargate_job_definition =  _batch.EcsJobDefinition(
            self,
            "EDM-JOB-DEFINITION",
            container= fargate_container_definition,
            job_definition_name="EDM-JOB-DEFINITION",
            retry_attempts= 2,

        )





        # Lets create the EDM Lambda
        edm_lambda = _lambda.Function(self, "EDMLambda",
                                      function_name= "EDM_APP_LAMBDA",
                                      runtime= _lambda.Runtime.PYTHON_3_11,
                                      code=_lambda.Code.from_asset("src"),
                                      handler="infraRunner.lambda_handler",
                                      role= existing_role
                                      )

