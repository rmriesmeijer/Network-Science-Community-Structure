"""
NetworkScienceCommunityDetection.py: Performs experiments using optimizers.

See the paper for specifics on choices.
"""

from cdlib import algorithms

from cdlib import NodeClustering

from networkx import nx

import warnings

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


def create_node_clustering(g, partition, name, method_params={}):
    """Return a clustering object for cdlib."""
    return NodeClustering(partition, g, name, method_params)


def benchmark_scores(samplesize=1):
    """Generate score data sets."""
    v = [0.1]#, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]

    f = open("benchmarks-opt1.csv", "w+")
    f.write("Spinglass, InfoMap, Leiden, Mu\n")

    # Read and evaluate graph optimizer scores for set 1.
    for mu in v:
        print(mu)
        for i in range(samplesize):
            filename = "./Graphs/lfr-graph{}-mu-{}.txt".format(i, mu)
            g = nx.read_gpickle(filename)
            scorespinglass = 0
            try:  # There is a probability the optimizers fail, indicated by -1
                scorespinglass = benchmark_score(g, algorithms.spinglass(g))
            except:
                scorespinglass = -1
            scoreinfomap = 0
            try:
                scoreinfomap = benchmark_score(g, algorithms.infomap(g))
            except:
                scoreinfomap = -1
            scoreleiden = benchmark_score(g, algorithms.leiden(g))
            vals = (scorespinglass, scoreinfomap, scoreleiden, mu)
            f.write("%f, %f, %f, %f\n" % vals)
            print("%f, %f, %f, %f" % vals)
    f.close()

    f = open("benchmarks-opt2.csv", "w+")
    f.write("Spinglass, InfoMap, Leiden, Mu\n")

    # Read and evaluate graph optimizer scores for set 2.
    for mu in v:
        print(mu)
        for i in range(samplesize):
            filename = "./Graphs/lfr2-graph{}-mu-{}.txt".format(i, mu)
            g = nx.read_gpickle(filename)
            scorespinglass = 0
            try:
                scorespinglass = benchmark_score(g, algorithms.spinglass(g))
            except:
                scorespinglass = -1
            scoreinfomap = 0
            try:
                scoreinfomap = benchmark_score(g, algorithms.infomap(g))
            except:
                scoreinfomap = -1
            scoreleiden = benchmark_score(g, algorithms.leiden(g))
            vals = (scorespinglass, scoreinfomap, scoreleiden, mu)
            f.write("%f, %f, %f, %f\n" % vals)
            print("%f, %f, %f, %f" % vals)
    f.close()


benchmark_scores()
