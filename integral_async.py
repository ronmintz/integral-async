import asyncio
import aioconsole

from math import sqrt
from math import pi

from time import time

duration_input = 0.0
duration_calc = 0.0

r = 10.0
start = -r
end = r
init_delta = 1.0
change_limit = 0.000_000_001
expected_result = pi * r**2 /2.0

def f(x):
    return sqrt(r**2 - x**2)

async def integrate(f, start, end, delta, change_limit):
    summ = 0.0

    x = start
    while x < end:
        summ += delta * (f(x) + f(x + delta)) / 2.0
        x += delta
    print(f"integrate(delta={delta}) = {summ}")
    return summ

async def integral(f, start, end, delta, change_limit):
    first_run = True
    prev_result = 0 # there is no previous result on the first run

    while True:
        result = await integrate(f, start, end, delta, change_limit)
        if not first_run and abs(result - prev_result) < change_limit:
            break
        prev_result = result
        delta  /= 2.0
        first_run = False

    print(f"\nintegral({delta}) = {result}")
    print("expected_result = ", expected_result)
    print("difference from expected_result = ", abs(expected_result - result))
    print("")
    return result

async def calc():
    global duration_calc
    print(f"start calc at {time()}")
    start_calc = time()
    await integral(f, start, end, init_delta, change_limit)
    duration_calc = time() - start_calc
    print(f"end calc at {time()}")


async def input1():
    global duration_input
    print(f"start input1 at {time()}")
    start_input = time()
    print("enter text: ")
    text = await aioconsole.ainput()
    duration_input = time() - start_input
    print(f"end input1 at {time()}")
    print("replay of text:", text)


async def tasks():
    print("async:\n")
    print(f"start tasks at {time()}")
    start_tasks = time()
    task1 = asyncio.create_task(input1())
    task2 = asyncio.create_task(calc())
    await asyncio.gather(task1, task2)
    duration_tasks = time() - start_tasks
    print(f"end tasks at {time()}")
    print("duration_input=", duration_input)
    print("duration_calc=", duration_calc)
    print("duration_tasks=", duration_tasks)
    print("sum of durations=", duration_input + duration_calc)
    print("duration_tasks - duration_calc=", duration_tasks - duration_calc)

if __name__ == "__main__":
    asyncio.run(tasks())
