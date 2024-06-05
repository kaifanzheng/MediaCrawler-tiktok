import random
import string
import time
import random
def generate_random_text(length=100):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
