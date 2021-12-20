from random import randint
import time


def get_random_num(num: int) -> str:
    rand_list = []
    for i in range(num):
        rand_list.append(str(randint(0, 9)))

    rand_str = "".join(rand_list)
    return rand_str


def get_timestemp() -> str:
    t = time.time()
    return str(int(t))
