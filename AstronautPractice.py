#!/bin/python3

import sys

class Node:
    def __init__(self, data):
        self.children = None
        self.parent = None
        self.discovered = False
        self.data = data

class Edge:
    def __init__(self, v1, v2):
        self.vertex1 = v1
        self.vertex2 = v2
        self.processed = False

class Graph:
    def init__(self, edges, vertices):
        self.edges = edges
        self.vertices = vertices

def getKey(item):
    return item[0]

#Compute the connected components
def components(inds, arr):
    start = arr[inds[0]]
    for a in arr:
        if (a != start and arr.index(a) not in inds) and (a[0] in start or a[1] in start):
            inds = [arr.index(a)] + inds
            #print(inds)
            return components(inds, arr)
    return inds

#Implement a recursive DFS on the graph to find the size of each component
#Note: Only built for one component at the moment
def DFS(G, v):
    if v.parent == None and v.children == None:
        ind = G.index(v)
        try:
            return DFS(G,G[ind+1])
        except:
            return 0   
    elif v.children:
        for child in v.children:
            if child.discovered == False:
                child.discovered = True
                print("child, " + repr(1))
                return 1 + DFS(G,child)
    elif v.parent:
        print(repr(v.data) + ", parent data = " + repr(v.parent.data)  + ", and parent discovered = " + repr(v.parent.discovered))
        if v.parent.discovered == False:
            v.parent.discovered = True
            print("parent, " + repr(1))
            return 1 + DFS(G,v.parent)
        else:
            print("Back to discovered parent, " + repr(-1))
            #v.parent.discovered = False
            return DFS(G,v.parent) 
    return 1
    

def journeyToMoon(n, astronaut):
    G = []
    for i in range(n):
        G.append(Node(i+1))
        
    for ast in astronaut:
        node1 = G[ast[0]-1]
        node2 = G[ast[1]-1]
        if node1.children:
            node1.children.append(node2)
        else:
            node1.children = [node2]
        if node2.children:
            node2.children.append(node1)
        else:
            node2.children = [node1]
        #node1.parent = node2
        #node2.parent = node1
    

    for v in G:
       print(repr(v.data))
       if v.children:
           print("Children: ")
           for child in v.children:
               print(" " + repr(child.data))

    G = Graph([], [])
    for i in range(n):
        G.vertices.append(Node(i+1))

    G[0].discovered = True
    return DFS(G, G[0])
    
                
        
if __name__ == "__main__":
    n, p = input().strip().split(' ')
    n, p = [int(n), int(p)]
    astronaut = []
    for astronaut_i in range(p):
       astronaut_t = [int(astronaut_temp) for astronaut_temp in input().strip().split(' ')]
       astronaut.append(astronaut_t)
    result = journeyToMoon(n, astronaut)
    print(result)
