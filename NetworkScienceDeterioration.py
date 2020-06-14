"""
NetworkScienceDeterioration.py: Performs experiments using deterioration.

See the paper for specifics on choices.
"""

from cdlib import NodeClustering

from networkx import nx

import random

import warnings

from cdlib import evaluation

from infomap import Infomap

warnings.simplefilter("ignore")


def benchmark_score(g, partition):
    """Return benchmark score function for given partition."""
    return real_partition(g).normalized_mutual_information(partition).score


def real_partition(g):
    """Return read out optimal partition and convert it to a clustering."""
    unvisited = [True] * len(g.nodes)
    result = []
    for i in range(len(g.nodes)):  # Visit all nodes and note their community.
        if unvisited[i]:
            part = list(g.nodes[i]['community'])
            result.append(part)
            for j in part:
                unvisited[j] = False
    return create_node_clustering(g, result, "Real")


def random_neighbor(g, part):
    """Return a partition that moves a random node to a random partition."""
    partition = part.communities
    new_partition = [[y for y in x] for x in partition]
    index = random.randint(0, len(partition) - 1)
    while len(partition[index]) == 0:  # Deal with empty partitions.
        index = random.randint(0, len(partition) - 1)
    part_index = random.randint(0, len(partition[index]) - 1)
    elem = partition[index][part_index]
    new_index = random.randint(0, len(partition) - 1)
    del new_partition[index][part_index]
    new_partition[new_index].append(elem)
    return create_node_clustering(g, new_partition, "Iteration")


def create_node_clustering(g, partition, name, method_params={}):
    """Return a clustering object for cdlib."""
    return NodeClustering(partition, g, name, method_params)


def eval_map_equation(g, partitionobj):
    """Return the map equation score for a given partition."""
    g1 = nx.convert_node_labels_to_integers(g, label_attribute="name")
    scoremapeq = 0
    partition = partitionobj.communities
    part = dict()
    for i in range(len(partition)):
        for ind in partition[i]:
            part[ind] = i
    im = Infomap("--silent --no-infomap")  # Don't change the partition.
    for e in g1.edges():
        im.addLink(e[0], e[1])
    im.initial_partition = part
    im.run()
    scoremapeq = im.codelength
    return scoremapeq


def benchmark_scores(samplesize=1):
    """Generate score data sets."""
    v = [0.1]#, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]

    f = open("benchmarks-det1.csv", "w+")
    f.write("Benchmark, Modularity, MapEquation, Iteration, Mu, GraphNum\n")

    # Read and evaluate graph deterioration scores for set 1.
    for mu in v:
        print(mu)
        for i in range(samplesize):
            filename = "./Graphs/lfr-graph{}-mu-{}.txt".format(i, mu)
            g = nx.read_gpickle(filename)
            part = real_partition(g)
            for j in range(1000):
                scorebench = benchmark_score(g, part)
                scoremod = evaluation.newman_girvan_modularity(g, part).score
                scoremapeq = eval_map_equation(g, part)
                vals = (scorebench, scoremod, scoremapeq, j, mu, i)
                f.write("%f, %f, %f, %d, %f, %d\n" % vals)
                if j == 0 or j == 500 or j == 999:
                    print("%f, %f, %f, %d, %f, %d" % vals)
                part = random_neighbor(g, part)
    f.close()

    f = open("benchmarks-det2.csv", "w+")
    f.write("Benchmark, Modularity, MapEquation, Iteration, Mu, GraphNum\n")

    # Read and evaluate graph deterioration scores for set 2.
    for mu in v:
        print(mu)
        for i in range(samplesize):
            filename = "./Graphs/lfr2-graph{}-mu-{}.txt".format(i, mu)
            g = nx.read_gpickle(filename)
            part = real_partition(g)
            for j in range(1000):
                scorebench = benchmark_score(g, part)
                scoremod = evaluation.newman_girvan_modularity(g, part).score
                scoremapeq = eval_map_equation(g, part)
                vals = (scorebench, scoremod, scoremapeq, j, mu, i)
                f.write("%f, %f, %f, %d, %f, %d\n" % vals)
                if j == 0 or j == 500 or j == 999:
                    print("%f, %f, %f, %d, %f, %d" % vals)
                part = random_neighbor(g, part)
    f.close()

benchmark_scores()
