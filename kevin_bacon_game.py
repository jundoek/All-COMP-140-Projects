"""
The Kevin Bacon Game.
"""

import simpleplot
import comp140_module4 as movies

class Queue:
    """
    A simple implementation of a FIFO queue.
    """
    
    def __init__(self):
        """ 
        Initialize the queue.
        """
        self._initialize_queue=[]
  
        

    def __len__(self):
        """
        Return number of items in the queue.
        """
        return len(self._initialize_queue)

    def __str__(self):
        """
        Returns a string representation of the queue.
        """
        return "A"
    
    def push(self, item):
        """
        Add item to the queue.
        """        
        self._initialize_queue.append(item)
        
    def pop(self):
        """
        Remove and return the least recently inserted item.
        Assumes that there is at least one element in the queue.  It
        is an error if there is not.  You do not need to check for
        this condition.
        """
      
        return self._initialize_queue.pop(0)
      
    
    def clear(self):
        """
        Remove all items from the queue.
        """
        self._initialize_queue=[]
        return self._initialize_queue




def bfs(graph, start_node):
    """
    Performs a breadth-first search on graph starting at the 
    start_node.
    Returns a two-element tuple containing a dictionary
    associating each visited node with the order in which it 
    was visited and a dictionary associating each visited node 
    with its parent node.
    """
    queue=Queue()
    dist={}
    parent={}
    
    for node in graph.nodes():
        dist[node]=float("inf")
        parent[node]=None 
    dist[start_node]=0
    queue.push(start_node)

    for node in graph.nodes():
        if len(queue)!=0:
            node2=queue.pop()
            for neighbor in graph.get_neighbors(node2): 
                if dist[neighbor]==float("inf"):
                    dist[neighbor]=dist[node2]+1
                    parent[neighbor]=node2
                    queue.push(neighbor)
    return dist, parent 

def distance_histogram(graph, node):
    """
    Given a graph and a node in that graph, returns a histogram
    (in the form of a dictionary mapping distance to counts) of
    the distances from node to every other node in the graph.
    """
    distance_counts={}
    bfs_result=bfs(graph, node)

    for other_node in bfs_result[0]:
        distance=bfs_result[0][node]-bfs_result[0][other_node]
        if distance<0:
            distance=0-distance

        if distance not in distance_counts.keys():
            distance_counts[distance]=0
            distance_counts[distance]+=1
        else:
            distance_counts[distance]+=1
              

    return distance_counts

def find_path(graph, start_person, end_person, parents):
    """
    Finds the path from start_person to end_person in the graph, 
    and returns the path in the form:
    [(actor1, set([movie1a, ...])), (actor2, set([movie2a, ...])), ...]
    """
    actor_movie=[]
    path=[]

    if  end_person==start_person:
        actor_movie=[start_person]+[set(path)]
        actor_movie=tuple(actor_movie)
        path.append(actor_movie)
        return path

    elif parents[end_person]==None:
        return path
    else:
        actor_movie=[end_person]+[set(path)]
        actor_movie=tuple(actor_movie)
        path.append(actor_movie)

        while end_person!=start_person:
            attribute=graph.get_attrs(parents[end_person],end_person)
            actor_movie=[parents[end_person]]+[attribute]
            actor_movie=tuple(actor_movie)
            path.append(actor_movie)
            end_person=parents[end_person]

    path.reverse()
    return path
  
   

def play_kevin_bacon_game(graph, start_person, end_people):
    """
    Play the "Kevin Bacon Game" on the actors in the given 
    graph, where startperson is the "Kevin Bacon"-esque 
    actor from which the search will start and endpeople 
    is a list of end people to which the search will be 
    performed.
    
    Prints the results out.
    """
    parents=bfs(graph,start_person)[1]
    for end_person in end_people:
        path=find_path(graph, start_person, end_person, parents) 
        movies.print_path(path)
def run():
    """
    Load a graph and play the Kevin Bacon Game.
    """
    graph5000 = movies.load_graph('subgraph5000')
    
    if len(graph5000.nodes()) > 0:
  
        play_kevin_bacon_game(graph5000, 'Kevin Bacon', 
            ['Amy Adams', 'Andrew Garfield', 'Anne Hathaway', 'Barack Obama', \
             'Benedict Cumberbatch', 'Chris Pine', 'Daniel Radcliffe', \
             'Jennifer Aniston', 'Joseph Gordon-Levitt', 'Morgan Freeman', \
             'Sandra Bullock', 'Tina Fey'])
        
        for person in ['Kevin Bacon', 'Stephanie Fratus']:
            hist = distance_histogram(graph5000, person)
            simpleplot.plot_bars(person, 400, 300, 'Distance', \
                'Frequency', [hist], ["distance frequency"])
 
# Uncomment the call to run below when you have completed your code.
# run()