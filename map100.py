from prefect import task, Flow


@task
def values():
    return [1] * 100


@task
def do_something(x):
    return x


with Flow("Map_100_halt_for_loop") as flow:
    v = values()
    do_something.map(v)

flow.run()
# flow.deploy(
#     image_name="map_100",
#     project_name="Demo",
#     local_image="python:3.7"
# )

