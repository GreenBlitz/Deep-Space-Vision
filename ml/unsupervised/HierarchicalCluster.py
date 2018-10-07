import numpy as np

def copy(x):
    if isinstance(x,np.ndarray):
        return x
    if isinstance(x, int) or isinstance(x, float):
        return x
    cp = []
    for i in x:
        cp.append(copy(i))
    return cp


def min_distance(x, y):
    m = np.Inf
    for i in x:
        for j in y:
            d = np.sum((i - j) ** 2)
            if d < m:
                m = d
    return np.sqrt(m)


def linear_mark(x, y):
    return min_distance(x, y)


def create_summing_mark(alpha=1.0, beta=1.0, gamma=1.0):
    def summing_mark(x, y):
        return alpha*min_distance(x, y) +\
            beta*min(len(x), len(y)) +\
            gamma*np.linalg.norm(np.array(x).sum(axis=0)/len(x) - np.array(y).sum(axis=0)/len(y))
    return summing_mark


def multiply_mark(x, y):
    return min_distance(x, y) *\
        min(len(x), len(y)) *\
        np.linalg.norm(np.array(x).sum(axis=0)/len(x) - np.array(y).sum(axis=0)/len(y))


def create_dependant_mark(alpha=1.0, beta=1.0, gamma=1.0):
    def dependant_mark(x, y):
        a = beta*min(len(x), len(y))
        b = gamma * np.linalg.norm(np.array(x).sum(axis=0) / len(x) - np.array(y).sum(axis=0) / len(y))
        c = alpha*min_distance(x, y)
        return a*b+a*c+c*a
    return dependant_mark


def hierarchical_cluster(inp, stamp_mark=linear_mark, min_c=None, max_c=None):
    """
    clusters the data with hierarchical clustering
    :param inp: data to cluster
    :param stamp_mark: the function used to determine the stamp mark for each cluster join
    the function accepts two arguments (cluster_a, cluster_b) which are both lists of vectors where all vectors in each
    cluster belong to the same cluster. the function returns the stamp mark of the join of the two clusters, meaning the
    cost of joining the two clusters.
    :param min_c: minimum amount of clusters
    :param max_c: maximum amount of clusters
    :return: an array of integers, each indicating the cluster of the input parameter with whom they share an index
    """
    prev_score = 0
    clusters = [[i] for i in inp]
    steps = [{"clusters": clusters}]

    if min_c is None:
        min_c = 1

    while len(clusters) > min_c:
        clusters = copy(clusters)
        join1, join2 = 0, 0
        min_score = np.Inf
        for i in range(len(clusters)):
            for j in range(i+1, len(clusters)):
                score = stamp_mark(clusters[i], clusters[j])
                if score < min_score:
                    min_score = score
                    join1 = i
                    join2 = j
        clusters[join1] += clusters[join2]
        del clusters[join2]
        steps.append({"clusters": clusters})
        steps[-2]['stamp_mark'] = min_score-prev_score
        prev_score = min_score

    steps = steps[:-1]

    if max_c is not None:
        steps = steps[max_c:]

    max_score = 0
    step = steps[0]['clusters']
    for i in steps:
        if i['stamp_mark'] > max_score:
            max_score = i['stamp_mark']
            step = i['clusters']

    def cluster_of(x):
        for i in range(len(step)):
            for j in step[i]:
                if (j == x).all():
                    return i

    return [cluster_of(x) for x in inp]
