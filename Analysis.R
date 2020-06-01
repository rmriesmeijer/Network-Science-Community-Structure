library(ggplot2)
library(dplyr)
library(hrbrthemes)
library(viridis)
library(cowplot)

# Read all the databases of the benchmarks.
benchmarks.det1 <- read.csv("~/GitHub/Network-Science-Community-Structure/benchmarks-det1.csv")
benchmarks.det2 <- read.csv("~/GitHub/Network-Science-Community-Structure/benchmarks-det2.csv")
benchmarks.opt1 <- read.csv("~/GitHub/Network-Science-Community-Structure/benchmarks-opt1.csv")
benchmarks.opt2 <- read.csv("~/GitHub/Network-Science-Community-Structure/benchmarks-opt2.csv")

# Define a normalization function.
range01 <- function(x){(x-min(x))/(max(x)-min(x))}

# benchmark
benchmarks.det1$BenchmarkNorm = range01(benchmarks.det1$Benchmark)
benchmarks.det1$ModularityNorm = range01(benchmarks.det1$Modularity)
benchmarks.det1$MapEquationNorm = range01(20 - benchmarks.det1$MapEquation)

# Add normalized scores to benchmark database 2.
benchmarks.det2$BenchmarkNorm = range01(benchmarks.det2$Benchmark)
benchmarks.det2$ModularityNorm = range01(benchmarks.det2$Modularity)
benchmarks.det2$MapEquationNorm = range01(20 - benchmarks.det2$MapEquation)

#Optional restriction filters.
#benchmarks.det1 = benchmarks.det1[benchmarks.det1$Mu == 0.7 & benchmarks.det1$GraphNum == 0,]
#benchmarks.opt2 = benchmarks.opt2[benchmarks.opt2$Spinglass >= 0 & benchmarks.opt2$InfoMap >= 0,]

# Aggregating data by taking the mean with respect to the iterations.
agg1 <- aggregate(benchmarks.det1, list(id11 = benchmarks.det1$Iteration), mean)
agg2 <- aggregate(benchmarks.det2, list(id11 = benchmarks.det2$Iteration), mean)

# Plot the normalized averages of the deterioration scores
# for the second set.
agg2$BenchmarkNorm = range01(agg2$Benchmark)
agg2$ModularityNorm = range01(agg2$Modularity)
agg2$MapEquationNorm = range01(20 - agg2$MapEquation)
p <- ggplot() + 
  geom_line(data = agg2, aes(x=Iteration, y = BenchmarkNorm, color="Benchmark")) + 
  geom_line(data = agg2, aes(x=Iteration, y = ModularityNorm, color="Modularity")) + 
  geom_line(data = agg2, aes(x=Iteration, y = MapEquationNorm, color="Map Equation")) + 
  ggtitle("Scores Per Iteration") + 
  ylab("Normalized scores") +
  scale_color_manual(values = c(
    'Benchmark' = '#444444',
    'Modularity' = '#D11141',
    'Map Equation' = '#00B159')) +
  labs(color = "Functions") +
  theme_ipsum()
print(p)

# Plot the normalized averages of the deterioration scores for the first set.
agg1$BenchmarkNorm = range01(agg1$Benchmark)
agg1$ModularityNorm = range01(agg1$Modularity)
agg1$MapEquationNorm = range01(20 - agg1$MapEquation)
p2 <- ggplot() + 
  geom_line(data = agg1, aes(x=Iteration, y = BenchmarkNorm, color="Benchmark")) + 
  geom_line(data = agg1, aes(x=Iteration, y = ModularityNorm, color="Modularity")) + 
  geom_line(data = agg1, aes(x=Iteration, y = MapEquationNorm, color="Map Equation")) + 
  ggtitle("Scores Per Iteration") + 
  ylab("Normalized scores") +
  scale_color_manual(values = c(
    'Benchmark' = '#444444',
    'Modularity' = '#D11141',
    'Map Equation' = '#00B159')) +
  labs(color = "Functions") +
  theme_ipsum()
print(p2)

# Filter negative values as they should have been 0;
# Namely, they return negative values incorrectly because the
# partition only has one community.
benchmarks.opt1$InfoMap[benchmarks.opt1$InfoMap < 0] <- 0
agg3 <- aggregate(benchmarks.opt1, list(id11 = benchmarks.opt1$Mu), mean)

# This maps negative values to 0 as described in the paper;
# As remarked another option is to use the filter defined earlier.
fix.negatives = benchmarks.opt2
fix.negatives$InfoMap[fix.negatives$InfoMap < 0] <- 0
fix.negatives$Spinglass[fix.negatives$Spinglass < 0] <- 0
fix.negatives$Leiden[fix.negatives$Leiden < 0] <- 0
agg4 <- aggregate(fix.negatives, list(id11 = fix.negatives$Mu), mean)

# Plot the benchmark scores of each optimizer for the first set.
p3 <- ggplot() + 
  geom_line(data = agg3, aes(x=Mu, y = InfoMap, color="InfoMap")) + 
  geom_line(data = agg3, aes(x=Mu, y = Leiden, color="Leiden")) + 
  geom_line(data = agg3, aes(x=Mu, y = Spinglass, color="Spinglass")) + 
  ggtitle("Mutual Information") + 
  ylab("Mutual Information") +
  scale_color_manual(values = c(
    'InfoMap' = '#444444',
    'Leiden' = '#D11141',
    'Spinglass' = '#00B159')) +
  labs(color = "Optimizer") +
  theme_ipsum()
print(p3)

# Plot the benchmark scores of each optimizer for the second set.
p4 <- ggplot() + 
  geom_line(data = agg4, aes(x=Mu, y = InfoMap, color="InfoMap")) + 
  geom_line(data = agg4, aes(x=Mu, y = Leiden, color="Leiden")) + 
  geom_line(data = agg4, aes(x=Mu, y = Spinglass, color="Spinglass")) + 
  ggtitle("Mutual Information") + 
  ylab("Mutual Information") +
  scale_color_manual(values = c(
    'InfoMap' = '#444444',
    'Leiden' = '#D11141',
    'Spinglass' = '#00B159')) +
  labs(color = "Optimizer") +
  theme_ipsum()
print(p4)

# Combine optimizer plots for side by side comparison.
p6 = plot_grid(p3, p4, labels = "Setups")
print(p6)

# Combine deterioration plots for side by side comparison.
p5 = plot_grid(p, p2, labels = "Setups")
print(p5)

# Compute the estimated probability that modularity is closer
# to the benchmark function with the method described in the
# paper for the first set.
benchmarks.det1$DMap <- abs(benchmarks.det1$MapEquationNorm - benchmarks.det1$BenchmarkNorm)
benchmarks.det1$DMod <- abs(benchmarks.det1$ModularityNorm - benchmarks.det1$BenchmarkNorm)
agg <- aggregate(benchmarks.det1, list(m = benchmarks.det1$Mu, g = benchmarks.det1$GraphNum), mean)
agg$PHat <- agg$DMap > agg$DMod
aggr <- aggregate(agg, list(m = agg$Mu), mean)
pHat1 <- aggr$PHat

# Compute the estimated probability that modularity is closer
# to the benchmark function with the method described in the
# paper for the second set.
benchmarks.det2$DMap <- abs(benchmarks.det2$MapEquationNorm - benchmarks.det2$BenchmarkNorm)
benchmarks.det2$DMod <- abs(benchmarks.det2$ModularityNorm - benchmarks.det2$BenchmarkNorm)
aggx <- aggregate(benchmarks.det2, list(m = benchmarks.det2$Mu, g = benchmarks.det2$GraphNum), mean)
aggx$PHat <- aggx$DMap > aggx$DMod
aggrx <- aggregate(aggx, list(m = aggx$Mu), mean)
pHat2 <- aggrx$PHat
