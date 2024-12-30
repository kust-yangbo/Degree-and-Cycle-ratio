
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


def get_smallest_cycles(Mygraph1):
    
    Mygraph = Mygraph1.copy()
    NodeNum=Mygraph.number_of_nodes()
    DEF_IMPOSSLEN = NodeNum + 1 
    SmallestCycles = set()
    NodeGirth = dict()
    NumSmallCycles = 0
    CycLenDict = dict()
    CycleRatio = {}

    SmallestCyclesOfNodes = {} 
    Coreness = nx.core_number(Mygraph)
    removeNodes =set()
    
    for i in Mygraph.nodes():  
        SmallestCyclesOfNodes[i] = set()
        CycleRatio[i] = 0
        if Mygraph.degree(i) <= 1 or Coreness[i] <= 1:
            NodeGirth[i] = 0
            removeNodes.add(i)
        else:
            NodeGirth[i] = DEF_IMPOSSLEN

    Mygraph.remove_nodes_from(removeNodes)  
    NumNode = Mygraph.number_of_nodes()  #update

    for i in range(3,Mygraph.number_of_nodes()+2):
        CycLenDict[i] = 0

    def my_all_shortest_paths(G, source, target):
        pred = nx.predecessor(G, source)
        if target not in pred:
            raise nx.NetworkXNoPath(
                f"Target {target} cannot be reached" f"from given sources"
            )
        sources = {source}
        seen = {target}
        stack = [[target, 0]]
        top = 0
        while top >= 0:
            node, i = stack[top]
            if node in sources:
                yield [p for p, n in reversed(stack[: top + 1])]
            if len(pred[node]) > i:
                stack[top][1] = i + 1
                next = pred[node][i]
                if next in seen:
                    continue
                else:
                    seen.add(next)
                top += 1
                if top == len(stack):
                    stack.append([next, 0])
                else:
                    stack[top][:] = [next, 0]
            else:
                seen.discard(node)
                top -= 1

    def getandJudgeSimpleCircle(objectList):#
        numEdge = 0
        for eleArr in list(itertools.combinations(objectList, 2)):
            if Mygraph.has_edge(eleArr[0], eleArr[1]):
                numEdge += 1
        if numEdge != len(objectList):
            return False
        else:
            return True

    NodeList = list(Mygraph.nodes())
    NodeList.sort()
    #setp 1
    curCyc = list()
    for ix in NodeList[:-2]:  #v1
        if NodeGirth[ix] == 0:
            continue
        curCyc.append(ix)
        for jx in NodeList[NodeList.index(ix) + 1 : -1]:  #v2
            if NodeGirth[jx] == 0:
                continue
            curCyc.append(jx)
            if Mygraph.has_edge(ix,jx):
                for kx in NodeList[NodeList.index(jx) + 1:]:      #v3
                    if NodeGirth[kx] == 0:
                        continue
                    if Mygraph.has_edge(kx,ix):
                        curCyc.append(kx)
                        if Mygraph.has_edge(kx,jx):
                            SmallestCycles.add(tuple(curCyc))
                            for i in curCyc:
                                NodeGirth[i] = 3
                        curCyc.pop()
            curCyc.pop()
        curCyc.pop()

    # setp 2
    ResiNodeList = []  # Residual Node List
    for nod in NodeList:
        if NodeGirth[nod] == DEF_IMPOSSLEN:
            ResiNodeList.append(nod)
    if len(ResiNodeList) == 0:
        pass
        #print("The smallest cycles of all nodes are 3-cycles, and there are no larger smallest cycles")
    else:
        visitedNodes = dict.fromkeys(ResiNodeList, set())
        for nod in ResiNodeList:
            for nei in list(Mygraph.neighbors(nod)):
                if nei not in visitedNodes.keys() or nod not in visitedNodes[nei]:
                    visitedNodes[nod].add(nei)
                    if nei not in visitedNodes.keys():
                        visitedNodes[nei] = set([nod])
                    else:
                        visitedNodes[nei].add(nod)
                    Mygraph.remove_edge(nod, nei)
                    if nx.has_path(Mygraph, nod, nei):
                        for path in my_all_shortest_paths(Mygraph, nod, nei):
                            lenPath = len(path)
                            path.sort()
                            SmallestCycles.add(tuple(path))
                            for i in path:
                                if NodeGirth[i] > lenPath:
                                    NodeGirth[i] = lenPath
                    Mygraph.add_edge(nod, nei)

    return SmallestCycles
