from prefect import task, Flow
from prefect.environments import RemoteEnvironment
from prefect.environments.storage import Docker


@task
def get_value():
    return "Example!"


@task
def output_value(value):
    print(value)


flow = Flow(
    "Local Executor Remote Example",
    environment=RemoteEnvironment(executor="prefect.engine.executors.LocalExecutor"),
    storage=Docker(registry_url="joshmeek18", image_name="flows",),
)

# set task dependencies using imperative API
output_value.set_upstream(get_value, flow=flow)
output_value.bind(value=get_value, flow=flow)

flow.deploy(project_name="Demo")
