from prefect import task, Flow
from prefect.environments import DaskKubernetesEnvironment


@task
def get_value():
    return "Example!"


@task
def output_value(value):
    print(value)


flow = Flow(
    "Min / Max Workers Dask Kubernetes Example",
    environment=DaskKubernetesEnvironment(min_workers=1, max_workers=3),
)

# set task dependencies using imperative API
output_value.set_upstream(get_value, flow=flow)
output_value.bind(value=get_value, flow=flow)
