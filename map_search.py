"""
Map Search
"""

import comp140_module7 as maps

class Queue:
    """
    A simple implementation of a FIFO queue.
    """
    def __init__(self):
        """
        Initialize the queue
        """
        self._items = []
    
    def __len__(self):
        """
        Return number of items in the queue.
        """
        return len(self._items)

    def __str__(self):
        """
        Return a string representing the queue.
        """
        return str(self._items)

    def push(self, item):
        """
        Add item to the queue.
        """        
        self._items.append(item)
    
    def pop(self):
        """
        Return and remove least recently inserted item.
        Assumes that there is at least one element in the queue.  It
        is an error if there is not.  You do not need to check for
        this condition.
        """
        return self._items.pop(0)
    
    def clear(self):
        """
        Remove all items from the queue.
        """
        self._items = []

class Stack:
    """
    A simple implementation of a LIFO stack.
    """
    def __init__(self):
        """ 
        Initialize the queue.
        """
        self._items = []

    def __len__(self):
        """
        Return number of items in the queue.
        """
        return len(self._items)

    def __str__(self):
        """
        Return a string representing the queue.
        """
        return str(self._items)

    def push(self, item):
        """
        Add item to the queue.
        """        
        self._items.append(item)
    
    def pop(self):
        """
        Return and remove least recently inserted item.
        Assumes that there is at least one element in the queue.  It
        is an error if there is not.  You do not need to check for
        this condition.
        """
        return self._items.pop(-1)
    
    def clear(self):
        """
        Remove all items from the queue.
        """
        self._items = []


def bfs_dfs(graph, rac_class, start_node, end_node):
    """
    Performs a breadth-first search or a depth-first search on graph
    starting at the start_node.  The rac_class should either be a
    Queue class or a Stack class to select BFS or DFS.

    Completes when end_node is found or entire graph has been
    searched.

    inputs:
        - graph: a directed Graph object representing a street map
        - rac_class: a restricted access container (Queue or Stack) class to
          use for the search
        - start_node: a node in graph representing the start
        - end_node: a node in graph representing the end

    Returns: a dictionary associating each visited node with its parent
    node.
    """
    rac=rac_class()
    dist = {}
    parent = {}
# initialize the parent and distance   
    for node in graph.nodes():
        dist[node] = float('inf')
        parent[node] = None

    dist[start_node] = 0
    rac.push(start_node)
# implement bfs or dfs search based on the recipe given for BFS search
    while len(rac)!=0:
        node = rac.pop()
        nbrs = graph.get_neighbors(node)
        for nbr in nbrs:
            if dist[nbr] == float('inf'):
                dist[nbr] = dist[node] + 1
                parent[nbr] = node
                rac.push(nbr)
# determine when to finish                   
                if nbr==end_node:
                    return parent
                    
                
    return parent 


def dfs(graph, start_node, end_node, parent):
    """
    Performs a recursive depth-first search on graph starting at the
    start_node.

    Completes when end_node is found or entire graph has been
    searched.

    inputs:
        - graph: a directed Graph object representing a street map
        - start_node: a node in graph representing the start
        - end_node: a node in graph representing the end
        - parent: a dictionary that initially has one entry associating
                  the original start_node with None

    Modifies the input parent dictionary to associate each visited node
    with its parent node
    """
    nbrs=graph.get_neighbors(start_node)
    key=parent.keys()
    counter=0
    for element1 in nbrs:
        if element1 not in key:
            counter=1
#   base case: start_node=end_node or the entire graph has been explored
    if start_node==end_node or counter==0:
        return parent
    else:
        for nbr in nbrs:
            if nbr not in key:
                parent[nbr]=start_node
                dfs(graph,nbr,end_node,parent)
        return parent        
    
def getkey(value,dict1):
    """
    This function is used to return the corresponding key for 
    the given value in a given dictionary 
    """
    for element in dict1.items():
        if element[1]==value:
            corr_key = element[0]
            return corr_key

def astar(graph, start_node, end_node,
          edge_distance, straight_line_distance):
    """
    Performs an A* search on graph starting at start_node.

    Completes when end_node is found or entire graph has been
    searched.

    inputs:
        - graph: a directed Graph object representing a street map
        - start_node: a node in graph representing the start
        - end_node: a node in graph representing the end
        - edge_distance: a function which takes two nodes and a graph
                         and returns the actual distance between two
                         neighboring nodes
        - straight_line_distance: a function which takes two nodes and
                         a graph and returns the straight line distance 
                         between two nodes

    Returns: a dictionary associating each visited node with its parent
    node.
    """
    open_set = []
    closed_set = []
    open_set.append(start_node)
    gcost = {start_node: 0}
    hcost = {start_node: straight_line_distance(start_node, end_node, graph)}
    parent = {start_node: None}
#   while openset is not empty
    while len(open_set) != 0:        
        min_node = open_set[0]
        min_f = gcost[min_node] + hcost[min_node]
        for node in open_set:
# 	check if the fcost is smaller than the minimum value, if so update the fcost 
            fcost = gcost[node] + hcost[node]
            if fcost < min_f:
                min_node = node
                min_f = fcost
#   if min_node is the end_node, end             
        if min_node == end_node:
            break
#   if min_node is not the end_node, 
#   remove min_node from the open_set and add
#   it to the closed_set
        open_set.remove(min_node)
        closed_set.append(min_node)
        for nbr in graph.get_neighbors(min_node):
# 	get the new gcost for the nbr node          
            new_gcost = gcost[min_node] + edge_distance(min_node, nbr, graph)
            if nbr in open_set:
                if new_gcost < gcost[nbr]:
                    gcost[nbr] = new_gcost
                    parent[nbr] = min_node
            elif (nbr not in open_set) and (nbr not in closed_set):
                open_set.append(nbr)
                parent[nbr] = min_node
                hcost[nbr] = straight_line_distance(nbr, end_node, graph)
                gcost[nbr] = new_gcost
    return parent             



maps.start(bfs_dfs, Queue, Stack, dfs, astar)
