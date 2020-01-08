# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#graph class using a dictionary implementation. 
#-An empty dictionary will be created upon instantation. 
#-Each node (key in the dictionary) has value as list containing the neighbors
#-The graph is undirected, so each of the neighbors will also be a key. 
class graph():
    def __init__(self):
        self.data = {}
        
    #If the node doesn't already exist in the graph, then add it
    def addNode(self, v):
        if v in self.data:
            print('node ' + str(v) + ' already in graph')
        else:
            self.data[v] = []
            
    #remove the specified vertex v from the graph. 
    #--Note we also have to remove it from the lists of neighbors whenever it 
    #appears. 
    def removeNode(self, v):
        if v not in self.data:
            print 'Node ' + str(v) + ' not in the graph'
        else:
            del self.data[v]
        for key in self.data:
            if v in self.data[key]:
                self.data[key].remove(v)
            
    #If u is not a node in the graph then add it and add v to the neighbors
    #If u does exist, then add v to the neighbors. 
    #If v doesn't exist, then add it and add u as a neighbor
    #If v does exist, then add u to its neighbors.
    def addNeighbor(self, u, v):
        if u not in self.data:
            self.data[u] = [v]
        else:
            self.data[u].append(v)
        if v not in self.data:
            self.data[v] = [u]
        else:
            self.data[v].append(u)
            
    #Return the graph data
    def getGraph(self):
        return self.data
    
     #depth first search on the graph starting at the input vertex v
    #-v: starting vertex
    #-visited: array to keep track of those vertices that have been visited.
    #-f_val: optional input, which is a destination node if we want to finda path
    #  between two nodes in the graph 
    def DFS(self, v, visited, f_val = None):
        for u in self.data[v]:   #self.data[v] == list of all neighbors of v
            if u == f_val:
                visited.append(u)
                return visited
            if u not in visited:
                if f_val not in visited:   #only recurse if f_val not found
                    visited.append(u)
                    self.DFS(u, visited, f_val)
                else:
                    return visited
        return visited
        
    
g = graph()
g.addNode(1)
g.addNode(3)
g.addNeighbor(1,10)
g.addNeighbor(3, 5)
g.addNeighbor(1, 3)
g.addNode(1)
g.addNode(10)
g.removeNode(10)
print(g.getGraph())
v = 4
print(g.DFS(v, [v]), 5)
