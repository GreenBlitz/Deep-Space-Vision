from functools import *


def split_list(lst, f, amount=2):
    """
    splits the list into several list according to the function f
    :param lst: the list to split
    :param f: a function which maps from an argument to the index of the list it should go to
    for example if we wanted a function to split a list into a list of positive and negative number f could look like
    lambda x: int(x >= 0)
    :param amount: the amount of lists to split the data to (2 by default)
    :return: a tuple of all the lists created,
    """
    tmp = tuple([] for _ in range(amount))
    for x in lst:
        tmp[f(x)].append(x)
    return tmp
