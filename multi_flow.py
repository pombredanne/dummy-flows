from prefect import task, Flow
from prefect.environments.storage import Docker


storage = Docker(registry_url="joshmeek18", image_name="my_flows", image_tag="v1")


@task
def extract():
    return [1, 2, 3]


@task
def transform(data):
    return [i * 10 for i in data]


@task
def load(data):
    print("Here's your data: {}".format(data))


with Flow("ETL") as etl_flow:
    e = extract()
    t = transform(e)
    l = load(t)


@task
def numbers_task():
    return [1, 2, 3]


@task
def map_task(x):
    return x + 1


@task
def reduce_task(x):
    return sum(x)


with Flow("Map / Reduce 🤓") as mr_flow:
    numbers = numbers_task()
    first_map = map_task.map(numbers)
    second_map = map_task.map(first_map)
    reduction = reduce_task(second_map)


storage.add_flow(etl_flow)
storage.add_flow(mr_flow)
storage = storage.build(push=False)

etl_flow.storage = storage
mr_flow.storage = storage

etl_flow.deploy(build="False")
mr_flow.deploy(build="False")