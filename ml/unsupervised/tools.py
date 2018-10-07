import numpy as np


def centers(x, c):
    cents = [np.zeros_like(x[0]) for _ in range(np.amax(c)+1)]
    _, counts = np.unique(c, return_counts=True)
    for i in range(len(c)):
        cents[c[i]] += x[i]
    for i in range(len(counts)):
        cents[i] /= counts[i]
    return cents


def split_by_clusters(x, c):
    a = [[] for _ in range(np.amax(c)+1)]
    for i in range(len(x)):
        a[c[i]].append(x[i])
    return a


def create_one_hot_labels(c, size=0):
    a = []
    size = max(np.amax(c)+1, size)
    for i in c:
        a.append(np.zeros(size,dtype=float))
        a[-1][i] = 1.0
    return a