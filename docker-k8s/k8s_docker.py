from prefect import Flow
from prefect.environments import KubernetesJobEnvironment
from prefect.environments.storage import Docker
from prefect.tasks.docker import (
    PullImage,
    CreateContainer,
    StartContainer,
    GetContainerLogs,
    WaitOnContainer,
)
from prefect.triggers import always_run



image = PullImage(
    docker_server_url="tcp://localhost:2375",
    repository="prefecthq/prefect",
    tag="latest",)
container = CreateContainer(
    docker_server_url="tcp://localhost:2375",
    image_name="prefecthq/prefect:latest",
    command='''python -c "from prefect import Flow; f = Flow('empty'); f.run()"''',
)
start = StartContainer(docker_server_url="tcp://localhost:2375",)
logs = GetContainerLogs(docker_server_url="tcp://localhost:2375", trigger=always_run)
status_code = WaitOnContainer(docker_server_url="tcp://localhost:2375",)

flow = Flow(
    "Run a Prefect Flow in Docker",
    environment=KubernetesJobEnvironment(job_spec_file="job_spec.yaml"),
    storage=Docker(
        registry_url="joshmeek18", image_name="flows", prefect_version="core_cloud_docs"
    ),
)

## set individual task dependencies using imperative API
container.set_upstream(image, flow=flow)
start.set_upstream(container, flow=flow, key="container_id")
logs.set_upstream(container, flow=flow, key="container_id")
status_code.set_upstream(container, flow=flow, key="container_id")

status_code.set_upstream(start, flow=flow)
logs.set_upstream(status_code, flow=flow)

flow.deploy(project_name="Demo")
