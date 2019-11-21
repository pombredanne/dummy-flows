from prefect import task, Flow

@task
def vals():
    return [1, 2, 3]

@task
def do_something(x):
    print(x * 10)
    return x * 10

@task
def final_task(y):
    print(sum(y))

with Flow('map') as f:
    v = vals()
    d = do_something.map(v)
    final_task(d)

f.run()
