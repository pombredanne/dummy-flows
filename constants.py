from prefect import task, Flow
from prefect.environments.storage import Docker


@task(name="Add")
def add_task(x, y):
    print(x + y)
    return x + y


with Flow(
    "add-example-v2", storage=Docker(registry_url="joshmeek18", image_name="flows"),
) as f:
    result = add_task(x=1, y=2)

f.deploy(project_name="Demo")
