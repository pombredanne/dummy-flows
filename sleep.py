from prefect import task, Flow
import time

@task
def sleep_task():
    for _ in range(10):
        time.sleep(86400)
    return "Done"


with Flow("Sleep_24_Hours") as flow:
    t = sleep_task()

# flow.run()
flow.deploy(
    registry_url="joshmeek18",
    image_name="flows",
    project_name="Demo"
)

