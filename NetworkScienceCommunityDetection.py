

from cdlib import algorithms

from cdlib import NodeClustering

from networkx import nx

from networkx.drawing.nx_pylab import draw_networkx

import matplotlib.pyplot as plt

import random

import math

import warnings

from cdlib import evaluation

from infomap import Infomap


# Benchmark score function for given partition.
def benchmark_score(G, partition):
    return real_partition(G).normalized_mutual_information(partition).score

# Read out the optimal partition from memory and convert it to a clustering.
def real_partition(G):
    unvisited = [True] * len(G.nodes)
    result = []
    for i in range(len(G.nodes)):
        if unvisited[i]:
            part = list(G.nodes[i]['community'])
            result.append(part)
            for j in part:
                unvisited[j] = False
    return create_node_clustering(G, result, "Real")

# Reassigns a random node to a random partition.
def random_neighbor(G, part):
    partition = part.communities
    new_partition = [[y for y in x] for x in partition]
    index = random.randint(0, len(partition) - 1)
    while len(partition[index]) == 0:
        index = random.randint(0, len(partition) - 1)
    part_index = random.randint(0, len(partition[index]) - 1)
    elem = partition[index][part_index]
    new_index = random.randint(0, len(partition) - 1)
    del new_partition[index][part_index]
    new_partition[new_index].append(elem)
    return create_node_clustering(G, new_partition, "")


# Converts a list of communities into a clustering object for networkx.
def create_node_clustering(G, partition, name, method_params={}):
    return NodeClustering(partition, G, name, method_params)


# Output results for analysis.
def benchmark_scores():
    f = open("benchmarks-opt1.csv","w+")
    f.write("Spinglass, InfoMap, Leiden, Mu\n")

    # Read and evaluate graph optimizer scores for set 1.
    for mu in [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]:
        print(mu)
        for i in range(50):
            filename = "./Graphs/lfr-graph{}-mu-{}.txt".format(i, mu)
            G = nx.read_gpickle(filename)
            num = len(real_partition(G).communities)
            scorespinglass = 0
            try:
                scorespinglass = benchmark_score(G, algorithms.spinglass(G))
            except:
                scorespinglass = -1
            scoreinfomap = 0
            try:
                scoreinfomap = benchmark_score(G, algorithms.infomap(G))
            except:
                scoreinfomap = -1
            scoreleiden = benchmark_score(G, algorithms.leiden(G))
            f.write("%f, %f, %f, %f\n" % (scorespinglass, scoreinfomap, scoreleiden, mu))
            print("%f, %f, %f, %f" % (scorespinglass, scoreinfomap, scoreleiden, mu))

    f.close()

    f = open("benchmarks-opt2.csv","w+")
    f.write("Spinglass, InfoMap, Leiden, Mu\n")

    # Read and evaluate graph optimizer scores for set 2.
    for mu in [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]:
        print(mu)
        for i in range(50):
            filename = "./Graphs/lfr2-graph{}-mu-{}.txt".format(i, mu)
            G = nx.read_gpickle(filename)
            num = len(real_partition(G).communities)
            scorespinglass = 0
            try:
                scorespinglass = benchmark_score(G, algorithms.spinglass(G))
            except:
                scorespinglass = -1
            scoreinfomap = 0
            try:
                scoreinfomap = benchmark_score(G, algorithms.infomap(G))
            except:
                scoreinfomap = -1
            scoreleiden = benchmark_score(G, algorithms.leiden(G))
            f.write("%f, %f, %f, %f\n" % (scorespinglass, scoreinfomap, scoreleiden, mu))
            print("%f, %f, %f, %f" % (scorespinglass, scoreinfomap, scoreleiden, mu))

    f.close()
    

    f = open("benchmarks-det1.csv","w+")
    f.write("Benchmark, Modularity, MapEquation, Iteration, Mu, GraphNum\n")

    # Read and evaluate graph deterioration scores for set 1.
    for mu in [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]:
        print(mu)
        for i in range(50):
            filename = "./Graphs/lfr-graph{}-mu-{}.txt".format(i, mu)
            G = nx.read_gpickle(filename)
            part = real_partition(G)
            for j in range(1000):
                scorebench = benchmark_score(G, part)
                scoremod = evaluation.newman_girvan_modularity(G, part).score
                scoremapeq = eval_map_equation(G, part)
                f.write("%f, %f, %f, %d, %f, %d\n" % (scorebench, scoremod, scoremapeq, j, mu, i))
                if j == 0 or j == 500 or j == 999:
                    print("%f, %f, %f, %d, %f, %d" % (scorebench, scoremod, scoremapeq, j, mu, i))
                part = random_neighbor(G, part)
    f.close()
    
    
    f = open("benchmarks-det2.csv","w+")
    f.write("Benchmark, Modularity, MapEquation, Iteration, Mu, GraphNum\n")

    # Read and evaluate graph deterioration scores for set 2.
    for mu in [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]:
        print(mu)
        for i in range(50):
            filename = "./Graphs/lfr2-graph{}-mu-{}.txt".format(i, mu)
            G = nx.read_gpickle(filename)
            part = real_partition(G)
            for j in range(1000):
                scorebench = benchmark_score(G, part)
                scoremod = evaluation.newman_girvan_modularity(G, part).score
                scoremapeq = eval_map_equation(G, part)
                f.write("%f, %f, %f, %d, %f, %d\n" % (scorebench, scoremod, scoremapeq, j, mu, i))
                if j == 0 or j == 500 or j == 999:
                    print("%f, %f, %f, %d, %f, %d" % (scorebench, scoremod, scoremapeq, j, mu, i))
                part = random_neighbor(G, part)
    f.close()
    
# Computes the map equation score for a given partition.
def eval_map_equation(G, partitionobj):
    g1 = nx.convert_node_labels_to_integers(G, label_attribute="name")
    scoremapeq = 0
    partition = partitionobj.communities
    part = dict()
    for i in range(len(partition)):
        for ind in partition[i]:
            part[ind] = i
    im = Infomap("--silent --no-infomap")
    for e in g1.edges():
        im.addLink(e[0], e[1])
    im.initial_partition = part
    im.run()
    scoremapeq = im.codelength
    return scoremapeq


benchmark_scores()