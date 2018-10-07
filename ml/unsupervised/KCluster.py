import numpy as np


def k_cluster(inp, k, max_iter=100, validate=True):
    clusters = [np.random.randint(k) for _ in inp]

    def distance(x, y):
        return np.sum((x-y)**2)

    def closest(x):
        ind = 0
        dist = distance(x, centers[0])
        for i in range(1, k):
            d = distance(x, centers[i])
            if d < dist:
                dist = d
                ind = i
        return ind

    if validate:
        for _ in range(max_iter):
            prev = np.copy(clusters)
            centers = [np.zeros_like(inp[0],dtype=float) for _ in range(k)]
            counts = list((0.0,)*k)
            for i in range(len(inp)):
                counts[clusters[i]] += 1
                centers[clusters[i]] += inp[i]
            for i in range(k):
                 centers[i] /= counts[i] if counts[i] > 0 else 1.0
            for i in range(len(inp)):
                clusters[i] = closest(inp[i])
            if (prev == np.array(clusters)).all():
                return clusters
    else:
        for _ in range(max_iter):
            centers = [np.zeros_like(inp[0]) for _ in range(k)]
            counts = list((0,)*k)
            for i in range(len(inp)):
                counts[i] += 1
                centers[i] += inp[i]
            for i in range(k):
                centers[i] /= float(counts[i])
            for i in range(len(inp)):
                clusters[i] = closest(inp[i])

    return clusters
