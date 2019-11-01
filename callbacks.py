from prefect import task
from prefect.environments import RemoteEnvironment


def starter():
    print("on_start---@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@---on_start")


def exiter():
    print("on_exit---######################################---on_exit")


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

with Flow(
    "Callbacks", environment=RemoteEnvironment(on_start=starter, on_exit=exiter)
) as flow:
    e = extract()
    t = transform(e)
    l = load(t)

flow.deploy(
    project_name="Demo",
    registry_url="joshmeek18",
    image_name="flows",
    prefect_version="environment_callbacks",
)
