
import re
import copy
import random
import collections
import scipy.io
import numpy as np
import networkx as nx
from tqdm import tqdm
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Calculate the cycle degree, and cycle ratio of nodes
def cyclesFeature(Mygraph, cycles):

    node_to_index = {node: index for index, node in enumerate(Mygraph.nodes())}
    cycles_number_matrix = np.zeros((Mygraph.number_of_nodes(), Mygraph.number_of_nodes()))

    for node, index in node_to_index.items():
        cycles_i = []
        for sub_cycles in cycles:
            if node in sub_cycles:
                cycles_i.append(sub_cycles)
        cycles_number_matrix[index][index] = len(cycles_i)
        cycles_node = [node_to_index[sub_node] for sub_cycles in cycles_i for sub_node in sub_cycles]
        cycles_dict = collections.Counter(cycles_node)
        cycles_num = dict(sorted(cycles_dict.items(), key=lambda x: x[0]))

        for j, count in cycles_num.items():
            cycles_number_matrix[index][j] = count
            cycles_number_matrix[j][index] = count

    cycles_degree = {}
    for node, index in node_to_index.items():
        cycles_degree[node] = cycles_number_matrix[index][index]

    cycles_ratio = {}
    for node, index in node_to_index.items():
        cycles_ratio[node] = 0
        ratio = 0
        for j in range(Mygraph.number_of_nodes()):
            if cycles_number_matrix[index][index] > 0 and cycles_number_matrix[index][j] > 0 and cycles_number_matrix[j][j] > 0:
                ratio += cycles_number_matrix[index][j] / cycles_number_matrix[j][j]
        cycles_ratio[node] = ratio

    sorted_cycles_degree = sorted(cycles_degree.items(), key=lambda item: item[1], reverse=True)
    sorted_cycles_ratio = sorted(cycles_ratio.items(), key=lambda item: item[1], reverse=True)

    return sorted_cycles_degree, sorted_cycles_ratio

# Calculate the degree of nodes
def node_degree(G):
    sorted_nodes_deg=sorted(G.degree(), key=lambda x: x[1], reverse=True)
    return sorted_nodes_deg 


# Define indicators DC: DC=a*degree+(1-a)*cycles_ratio
def Weighted_list(Mygraph, a, sorted_cycles_ratio, sorted_nodes_deg):  

    deg_dict = dict(sorted_nodes_deg)
    new_list = []
    for node, value in sorted_cycles_ratio:
        new_value = a * deg_dict[node] + (1 - a) * value
        new_list.append((node, new_value))
    Weighted_list = sorted(new_list, key=lambda x: x[1], reverse=True) 
    
    return Weighted_list


