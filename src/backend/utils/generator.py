import random


def gen_id(length: int) -> str:
    id = ""
    
    for _ in range(length):
        id += str(random.randint(1, 9))
    
    return id