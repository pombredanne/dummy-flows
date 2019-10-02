from prefect import task, Flow
from prefect.engine.result_handlers import JSONResultHandler
import datetime

@task(max_retries=2, retry_delay=datetime.timedelta(minutes=2))
def failing_task(inputs):
    print(inputs)
    raise Exception("Attempting retry")

with Flow("retry-test", result_handler=JSONResultHandler()) as flow:
    failing_task(inputs=[1,2,3,4,5])

flow.deploy(project_name='Demo', registry_url="joshmeek18", image_name="flows")