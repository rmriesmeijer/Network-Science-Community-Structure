"""
LFRNetworkGenerator.py: Generates graph for the experiments.

The parameters are chosen along the lines of convention in research.
"""

from networkx.generators.community import LFR_benchmark_graph

from networkx import nx

# Generator for the first set of benchmarks.
samplesize = 1
mus = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
for mu in mus:
    print(mu)
    i = 0
    errored = False
    while True:
        if i == samplesize:
            break
        # Somehow sometimes the generator breaks.
        try:
            G = LFR_benchmark_graph(1000,  # Number of nodes in graph.
                                    3,     # Exponent of the distribution.
                                    1.1,   # Exponent for community sizes.
                                    mu,    # Mixing parameter.
                                    max_degree=50,
                                    average_degree=10,
                                    min_community=10,
                                    max_community=50)
            filename = "./Graphs/lfr-graph{}-mu-{}.txt".format(i, mu)
            nx.write_gpickle(G, filename)

            i = i + 1
        except:
            errored = True

# Generator for the second set of benchmarks.
mus = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
for mu in mus:
    print(mu)
    i = 0
    errored = False
    while True:
        if i == samplesize:
            break
        # Somehow sometimes the generator breaks.
        try:
            G = LFR_benchmark_graph(1000,  # Number of nodes in graph.
                                    3,     # Exponent of the distribution.
                                    1.5,   # Exponent for community sizes.
                                    mu,    # Mixing parameter.
                                    average_degree=6,
                                    min_community=23)
            filename = "./Graphs/lfr2-graph{}-mu-{}.txt".format(i, mu)
            nx.write_gpickle(G, filename)

            i = i + 1
        except:
            errored = True
