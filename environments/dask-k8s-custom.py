from prefect import task, Flow
from prefect.environments import DaskKubernetesEnvironment
from prefect.environments.storage import Docker


@task
def get_value():
    return "Example!"


@task
def output_value(value):
    print(value)


flow = Flow(
    "Custom Worker Spec Dask Kubernetes Example",
    environment=DaskKubernetesEnvironment(worker_spec_file="worker_spec.yaml"),
    storage=Docker(
        registry_url="joshmeek18", image_name="flows", image_tag="qqq", python_dependencies=["kubernetes==10.0.1"]
    ),
)

# set task dependencies using imperative API
output_value.set_upstream(get_value, flow=flow)
output_value.bind(value=get_value, flow=flow)

# print(flow.environment._worker_spec)

flow.deploy(project_name="Demo", prefect_version="master")
# out = flow.save()

# Flow.load()