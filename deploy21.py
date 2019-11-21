from prefect import task, Flow

@task(name="Add")
def add_task(x, y):
    print(x + y)
    return x + y


with Flow(
    "Deploy21",
) as f:
    result = add_task(x=1, y=2)

f.deploy(project_name="Demo", labels=["yes"])

f.run_agent()