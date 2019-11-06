from prefect import task, Flow
from prefect.environments import KubernetesJobEnvironment
from prefect.environments.storage import Docker


@task
def get_value():
    return "Example!"


@task
def output_value(value):
    print(value)


flow = Flow(
    "Kubernetes Job Environment w/ Resource Requests & Limits",
    environment=KubernetesJobEnvironment(job_spec_file="job_spec.yaml"),
    storage=Docker(
        registry_url="joshmeek18", image_name="flows"
    ),
)

# set task dependencies using imperative API
output_value.set_upstream(get_value, flow=flow)
output_value.bind(value=get_value, flow=flow)
