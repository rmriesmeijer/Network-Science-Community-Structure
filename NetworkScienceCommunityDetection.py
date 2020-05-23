from networkx import nx

from networkx.drawing.nx_pylab import draw_networkx

import matplotlib.pyplot as plt

import random

import math

from cdlib import algorithms

# For visualization.
limits = plt.axis('off') # turn of axis

# Benchmark score function for given partition.
def benchmark_score(G, partition):
    score = 0.0
    best = real_partition(G)


    return score

def real_partition(G):
    unvisited = [True] * len(G.nodes)
    result = []
    for i in range(len(G.nodes)):
        if unvisited[i]:
            part = list(G.nodes[i]['community'])
            result.append(part)
            for j in part:
                unvisited[j] = false
    return result


# Simulated annealing k partitions on network for goal function.
def simulated_annealing_partitions(G, num_partitions, goalfunction):
    s = random_start(G, num_partitions)
    score = 0
    T = 1.001
    diff = 1
    while T < 0.002 or diff < 0.01:
        x = random_neighbor(s)
        new_score = goalfunction(G, x)
        r = random.uniform(0, 1)
        diff = new_score - score if new_score > score else 1
        if score >= new_score or r <= exp((score - new_score) / T):
            score = new_score
            s = x
        T -= 0.001
    return s, score

def random_start(G, num_partitions):
    result = [[]]*num_partitions
    for i in range(len(G.nodes)):
        result[i % num_partitions].append(i)
    return result

def random_neighbor(partition):
    new_partition = partition[:][:]
    index = random.randint(0, len(partition) - 1)
    part_index = random.randomint(0, len(partition[index]) - 1)
    elem = partition[index][part_index]
    new_index = random.randint(0, len(partition) - 1)
    del new_partition[index][part_index]
    new_partition[new_index].append(elem)
    return new_partition

# Output results for analysis.
def benchmark_scores():
    graph_set = []
    graph_set_params = []
    scores_modularity = []
    scores_goalfunction = []
    scores_infomap = []
    scores_ownfunction = []

    # Read and evaluate graphs.
    for mu in [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]:
        for i in range(20):
            filename = "./Graphs/lfr-graph{}-mu-{}.txt".format(i, mu)
            G = nx.read_gpickle(filename)
            print(algorithms.infomap(G))

    return graph_set, graph_set_params, scores_modularity, scores_goalfunction, scores_infomap, scores_goalfunction

# Modularity function for given partition.
def modularity_score(G, partition):
    score = 0.0

    return score

# Infomap function for given partition.
def infomap_score(G, partition):
    score = 0.0

    return score

# Own community score for given partition.
def ownfunction_score(G, partition):
    score = 0.0

    return score

benchmark_scores()