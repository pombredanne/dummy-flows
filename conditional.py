from prefect import task, Flow, Parameter
from prefect.tasks.control_flow import ifelse


@task
def check_if_even(value):
    return (value % 2 == 0)


@task
def print_odd(value):
    print("{} is odd!".format(value))


@task
def print_even(value):
    print("{} is even!".format(value))


with Flow("Check Even/Odd") as f:
    value = Parameter("value")
    is_even = check_if_even(value)

    even = print_even(value)
    odd = print_odd(value)

    ifelse(is_even, even, odd)

