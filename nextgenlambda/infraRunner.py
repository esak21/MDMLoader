
import boto3

def create_client():
    _batch_client  = boto3.client("batch")
    return _batch_client

def register_my_job(batch_client):
    batch_client.register_job_definition(
        jobDefinitionName = "EDM-JOB",
        type = "container",
        schedulingPriority=10,
    )
def create_job_queue(batch_client):
    response = batch_client.create_job_queue(
        jobQueueName='EDM-ANALYZER-QUEUE',
        state='ENABLED',
        priority=10,
        computeEnvironmentOrder=[
            {
                'order': 10,
                'computeEnvironment': 'EDM-ANALYZER'
            }
        ]
    )
    return response

def create_job_compute(batch_client):
    compute_resources_payload = {
        'type' : 'FARGATE_SPOT',
        'maxvCpus': 20,
        'subnets': [
            'subnet-0978bf45835ebba06', 'subnet-0d8c348525119d2e3' ,'subnet-09a5c681fd9c8ee99'
        ],
        'securityGroupIds': [
            'sg-0ece7828869b52df5'
        ],

    }
    response = batch_client.create_compute_environment(
        computeEnvironmentName='EDM-ANALYZER',
        type='MANAGED',
        state= 'ENABLED',
        serviceRole='arn:aws:iam::905418448077:role/aws-service-role/batch.amazonaws.com/AWSServiceRoleForBatch',
        computeResources = compute_resources_payload ,
        tags={
            'app': 'EDM'
        },

    )

    print("Compute Job created successfully")

    return response


def lambda_handler(event, context):
    print(event)
    print("we are going to spin up the AWS Batch instances")
    batch_client = create_client()
    response = create_job_compute(batch_client)
    print(response)

    # Create the Job Queue
    job_queue_response  = create_job_queue(batch_client)
    print(job_queue_response)

    # Create Job Definition

    print(context)