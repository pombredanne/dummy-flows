from prefect import task


@task
def extract():
    """Get a list of data"""
    return [1, 2, 3]


@task
def transform(data):
    """Multiply the input by 10"""
    return [i * 10 for i in data]


@task
def load(data):
    """Print the data to indicate it was received"""
    import prefect
    logger = prefect.context.get("logger")
    logger.info("Here")
    print("Here's your data: {}".format(data))


from prefect import Flow

with Flow("ETL") as flow:
    e = extract()
    t = transform(e)
    l = load(t)

from prefect.engine.executors import DaskExecutor

# from dask.distributed import LocalCluster
# cluster = LocalCluster()

executor = DaskExecutor(address="localhost:8786")
flow.run(executor=executor)