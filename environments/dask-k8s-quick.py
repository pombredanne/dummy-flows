from prefect import task, Flow
from prefect.environments import DaskKubernetesEnvironment


@task
def get_value():
    return "Example!"


@task
def output_value(value):
    print(value)


flow = Flow(
    "dk8s-debug",
    environment=DaskKubernetesEnvironment(min_workers=2, max_workers=4),
)

# set task dependencies using imperative API
output_value.set_upstream(get_value, flow=flow)
output_value.bind(value=get_value, flow=flow)

flow.deploy(
    "Demo", registry_url="joshmeek18", image_name="flows", prefect_version="master"
)

