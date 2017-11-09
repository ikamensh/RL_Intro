import random
from time import time
from matplotlib import pyplot as plt




def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        upto += w
        if upto >= r:
            return c

    assert False, "Shouldn't get here"


def draw_2darray(array, filename):
    plt.clf()
    plt.imshow(array)
    plt.colorbar()
    plt.savefig(filename)


t = time()


def timestamp(i, delta):
    global t
    dt = time() - t
    t = time()
    print("iteration {} done in {} sec, causing change in values = {}".format(i, dt, delta))