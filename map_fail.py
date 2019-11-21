from prefect import task, Flow
from prefect.triggers import any_successful


@task
def divide(x):
    return 1 / x


@task(trigger=any_successful)
def aggregate(results):
    print(results)


with Flow("divide-fail") as flow:
    results = divide.map([0, 1, 2])
    aggregate(results)

flow.run()
