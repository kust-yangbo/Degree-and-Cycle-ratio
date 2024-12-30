
import re
import copy
import random
import collections
import scipy.io
import numpy as np
from tqdm import tqdm
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib.font_manager import FontProperties

import SmallestCycles
from SmallestCycles import *
import DC_function
from DC_function import *

# Calculation of relative size of the largest connected subgraph
def largest_component_ratio(G):
    components = list(nx.connected_components(G))  
    if not components:
        ratio = 0.0
    else:
        largest_component = max(components, key=len)  
        largest_component_size = len(largest_component)  
        ratio = largest_component_size / N  
    return ratio

# Remove nodes in descending order of indicators
def remove_top_k_nodes_cycles_ratio(G, k, Weighted_list): 

    if Weighted_list:
        nodes_to_remove = [node[0] for node in Weighted_list[:k]]
        G1 = G.copy()
        G1.remove_nodes_from(nodes_to_remove)
        return G1
    else:
        G1 = nx.Graph()        
        return G1

def cycles_ratio_remove_g(G, weighted_list):
    g = [] 
    for i in range(0, G.number_of_nodes()+1):
        G1 = remove_top_k_nodes_cycles_ratio(G, i, weighted_list)
        gn = largest_component_ratio(G1)
        g.append(gn)
    
    R = sum(g) / N 
    return g, R


NetworkAddress = r'Email.txt'
networkName = 'Email'
Mygraph = nx.Graph()
rawC = 0
file = open(NetworkAddress)
while 1:
    lines = file.readlines(10000)
    if not lines:
        break
    for line in lines:
        #input format of the network
        line = line[:-1]
        Mygraph.add_edge(int(line[:6]), int(line[7:]))
file.close()

NodeNum = Mygraph.number_of_nodes()  
N = Mygraph.number_of_nodes()  
Mygraph.remove_edges_from(nx.selfloop_edges(Mygraph))

sorted_nodes_deg=node_degree(Mygraph)
SmallestCycles = get_smallest_cycles(Mygraph)
sorted_cycles_degree, sorted_cycles_ratio=cyclesFeature(Mygraph, SmallestCycles)

weighted_list=Weighted_list(Mygraph, 0.6, sorted_cycles_ratio, sorted_nodes_deg)
g, R = cycles_ratio_remove_g(Mygraph, weighted_list)
print(g)