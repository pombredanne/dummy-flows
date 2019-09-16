import yaml

from prefect import Flow
from prefect.tasks.kubernetes import CreateNamespacedJob, DeleteNamespacedJob

with open("example_job.yaml") as file:
    job = yaml.safe_load(file)

job_task = CreateNamespacedJob()
delete_task = DeleteNamespacedJob()

with Flow("asdf") as f:
    t1 = job_task(body=job)
    t2 = delete_task(job_name="pi")

f.run()

