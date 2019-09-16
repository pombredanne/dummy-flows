import requests

from prefect import context, task, Flow, Parameter
from prefect.engine.signals import LOOP


@task
def fizz_buzz(N):
    loop_payload = context.get("task_loop_result", {})

    n = loop_payload.get("n", N)

    out = requests.get(
        f"http://fibuzzapi.herokuapp.com/api/numbers?offset={n}&limit=1"
    ).json()["numbers"][0]["value"]

    if n == 1:
        return out

    raise LOOP(message=f"{n}={out}", result=dict(n=n - 1))


with Flow("FizzBuzz") as flow:
    N = Parameter("N")
    fizzbuzz = fizz_buzz(N)

flow_state = flow.run(N=100)

