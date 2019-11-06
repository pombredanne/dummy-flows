from prefect import task, Flow
from prefect.environments import FargateTaskEnvironment
from prefect.environments.storage import Docker


@task
def get_value():
    return "Example!"


@task
def output_value(value):
    print(value)


flow = Flow(
    "Fargate Task Environment",
    environment=FargateTaskEnvironment(
        aws_session_token="MY_AWS_SESSION_TOKEN",
        region="us-east-1",
        cpu="256",
        memory="512",
        networkConfiguration={
            "awsvpcConfiguration": {
                "assignPublicIp": "ENABLED",
                "subnets": ["MY_SUBNET_ID"],
                "securityGroups": ["MY_SECURITY_GROUP"],
            }
        },
        family="my_flow",
        taskRoleArn="MY_TASK_ROLE_ARN",
        executionRoleArn="MY_EXECUTION_ROLE_ARN",
        containerDefinitions={
            "name": "flow-container",
            "image": "image",
            "command": [],
            "environment": [],
            "essential": True,
        }
    ),
    storage=Docker(registry_url="joshmeek18", image_name="flows"),
)

# set task dependencies using imperative API
output_value.set_upstream(get_value, flow=flow)
output_value.bind(value=get_value, flow=flow)

