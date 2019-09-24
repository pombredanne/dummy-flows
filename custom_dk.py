from prefect import task, Flow
from prefect.environments.execution import DaskKubernetesEnvironment
from prefect.environments.storage import Docker


@task
def first_task():
    return [100] * 100


@task
def compute(x):
    return x * 100


with Flow(
    "CDK",
    environment=DaskKubernetesEnvironment(
        scheduler_spec_file="./scheduler.yaml",
        worker_spec_file="./worker.yaml",
    ),
    storage=Docker(
        registry_url="joshmeek18",
        image_name="flows",
        image_tag="cdk",
        prefect_version="dk_custom",
    ),
) as flow:
    one = first_task()
    result = compute.map(one)

flow.deploy(project_name="Demo")
