import distributed
import time
from prefect import task, Flow
from prefect.environments import DaskKubernetesEnvironment
from prefect.environments.storage import Docker


@task
def add(x, y):
    with distributed.worker_client():
        time.sleep(30 * 60)
    return x + y


with Flow(
    "zombie",
    environment=DaskKubernetesEnvironment(),
    storage=Docker(
        registry_url="joshmeek18",
        image_name="flows",
        prefect_version="master"
    ),
) as flow:
    add(add(1, 2), add(2, 3))

flow.deploy(project_name="Demo")