import string
import random


def generate_random_name():
    rand_name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=7))
    return rand_name
