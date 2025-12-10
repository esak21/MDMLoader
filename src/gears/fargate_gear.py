from constructs import Construct
from aws_cdk import (
    aws_batch as _batch,
    aws_ec2 as _ec2,
    aws_ecs as _ecs,
aws_iam as _iam ,
    Size
)

from src.infra.my_stack_props import BATCHGearprops


class FargateGear(Construct):

    def __init__(self, scope: Construct, id: str, props: BATCHGearprops, **kwargs):
        super().__init__(scope, id, **kwargs)

        app_vpc = _ec2.Vpc.from_lookup(
            self,
            "DefaultVpcLookup",
            is_default=True
        )

        existing_batch_tasks_role_arn = "arn:aws:iam::905418448077:role/MyBatchJoBRoles"
        existing_batch_tasks_role = _iam.Role.from_role_arn(self, "EDM_BATCH-TASK-INFRA-ROLE", existing_batch_tasks_role_arn, mutable=False)
        existing_batch_tasks_execution_role_arn = "arn:aws:iam::905418448077:role/BatchEcsTaskExecutionRole"
        existing_batch_tasks_execution_role = _iam.Role.from_role_arn(self, "EDM_BATCH-TASK-INFRA-EXE-ROLE",
                                                            existing_batch_tasks_execution_role_arn, mutable=False)


        # Create the batch Compute Environment Via L1
        app_batch_compute = _batch.CfnComputeEnvironment(
            self,
            "EDM-OLAP",
            compute_environment_name= "EDM-APP-COMPUTE",
            type= "MANAGED",
            state= "ENABLED",

            compute_resources= _batch.CfnComputeEnvironment.ComputeResourcesProperty(
                maxv_cpus= 16 ,
                type= "FARGATE",
                subnets= ["subnet-0978bf45835ebba06", "subnet-0d89fb196a80536c0", "subnet-09a5c681fd9c8ee99"],
                security_group_ids=[
                   "sg-0ece7828869b52df5"
                ],

            )

        )


        print(f"INFO : batch Compute resources are created {app_batch_compute.to_string}")

        app_job_queue = _batch.CfnJobQueue(
            self,
            "EDM-OLAP-QUEUE",
            job_queue_name= "EDM-OLAP-QUEUE",
            priority= 1,
            compute_environment_order= [
                _batch.CfnJobQueue.ComputeEnvironmentOrderProperty(
                    compute_environment= "EDM-APP-COMPUTE",
                    order= 1
                )
            ]
        )
        app_container_property = _batch.CfnJobDefinition.ContainerPropertiesProperty(
            image= "public.ecr.aws/e5n9j2q9/edm",
            log_configuration= _batch.CfnJobDefinition.LogConfigurationProperty(
                log_driver= "awslogs",
                options= {
                    "awslogs-group": "/ecs/EDM-OLAP-Job-DEFINITION",
                    "awslogs-region": "us-east-1",
                    "awslogs-stream-prefix": "EDM-OLAP-Job-DEFINITION"
                }
            ),
            resource_requirements= [
                _batch.CfnJobDefinition.ResourceRequirementProperty(
                    type= "VCPU",
                    value= "0.25"
                ),
                _batch.CfnJobDefinition.ResourceRequirementProperty(
                    type= "MEMORY",
                    value= "512"
                )
            ],
            job_role_arn = existing_batch_tasks_role.role_arn,
            execution_role_arn= existing_batch_tasks_execution_role.role_arn,
            environment=  [ _batch.CfnJobDefinition.EnvironmentProperty(name="env",value="qa") ,
                            _batch.CfnJobDefinition.EnvironmentProperty(name="app", value="automation"),
                            ],
            command = ["python", "src/runner.py" , "gym_membership.csv"],
            network_configuration= _batch.CfnJobDefinition.NetworkConfigurationProperty(
                assign_public_ip= "ENABLED"
            )
        )

        app_job_df = _batch.CfnJobDefinition(
            self,
            "EDM-OLAP-QUEUE-JD",
            type= "container",
            platform_capabilities= ["FARGATE"],
            job_definition_name= "EDM-OLAP-Job-DEFINITION",
            container_properties= app_container_property
        )
        print(f"INFO JOb Definition created {app_job_df.stack}")

        app_job_queue.add_depends_on(app_batch_compute)
        app_job_df.add_depends_on(app_job_queue)