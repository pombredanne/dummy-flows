from prefect import task
from prefect.environments.storage import Docker
from prefect.environments import FargateTaskEnvironment


@task
def extract():
    """Get a list of data"""
    return [1, 2, 3]


@task
def transform(data):
    """Multiply the input by 10"""
    return [i * 10 for i in data]


@task
def load(data):
    """Print the data to indicate it was received"""
    print("Here's your data: {}".format(data))


from prefect import Flow

with Flow("ETL-fte", environment=FargateTaskEnvironment(), storage=Docker(base_image="prefecthq/prefect:latest")) as flow:
    e = extract()
    t = transform(e)
    l = load(t)

flow.storage.add_flow(flow)
flow.storage.build()
# flow.deploy(project_name="Demo", registry_url="joshmeek18", image_name="flows")