from prefect.engine.executors import DaskExecutor
from prefect import Flow, task

import random

@task
def numbers_task():
    return [random.randint(1, 1000)] * 100


@task
def map_task(x):
    return x + 1


@task
def reduce_task(x):
    return sum(x)


with Flow("Map / Reduce (hey twitter)") as flow:
    numbers = numbers_task()
    first_map = map_task.map(numbers)
    second_map = map_task.map(first_map)
    reduction = reduce_task(second_map)

flow.run(executor=DaskExecutor("tcp://192.168.1.31:8786"))

