from time import time
import random

from django.utils import timezone



def generate_oin():
    """
    return 18 digit random char
    """
    now = timezone.now()
    first = now.strftime("%y%m%d")
    # second = "".join([str(random.randint(0,9)) for i in range(12)])
    second = str(random.random()).split('.')[1][:12]
    oin = first + second
    return oin


def find_match(times):
    li = []
    count = 0
    for i in range(times):
        oin = generate_oin()
        if oin in li:
            count += 1
        li.append(oin)
    print(count)

