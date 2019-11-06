from prefect import task, Flow
from prefect.environments.storage import Docker


@task
def values():
    return [1] * 100


@task
def do_something(x):
    return x


with Flow(
    "Map_100_master",
    storage=Docker(
        registry_url="joshmeek18", image_name="flows", prefect_version="master"
    ),
) as flow:
    v = values()
    do_something.map(v)

flow.deploy(project_name="Demo")

