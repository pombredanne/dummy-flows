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
    "dktest",
    environment=DaskKubernetesEnvironment(min_workers=1, max_workers=3),
    storage=Docker(registry_url="joshmeek18", image_name="flows"),
) as flow:
    one = first_task()
    result = compute.map(one)
    result2 = compute.map(one)
    result3 = compute.map(one)

# flow.deploy(project_name="Demo")
flow.visualize()
