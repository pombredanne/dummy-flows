
from prefect import task, Flow
from prefect.tasks.control_flow import switch

@task
def condition():
    return "b"

@task
def a_branch():
    return "A Branch"

@task
def b_branch():
    return "B Branch"

with Flow("switch-flow") as flow:
    switch(condition, dict(a=a_branch, b=b_branch))

flow.run()