#!/bin/bash

# Generate graphs.
pip install networkx==2.4
python -m LFRNetworkGenerator.py

# Optimization data generation.
pip install cdlib[C]
python -m NetworkScienceCommunityDetection.py

# Deterioration data generation.
pip install infomap --upgrade
python -m NetworkScienceDeterioration.py
