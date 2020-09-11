# Graph-Algorithm-Visualizer


## Description
This is a graph algorithm visualizer. Note that the grid can be viewed as a directed graph where every single edge between neighboring cells exists and the weight of the edge going from cell A to cell B is the weight of cell B. All of the nodes on the grid start off with a weight of 1. Also note that each of the algorithms can handle different types of graphs (this will be covered below) A few things are changed from the normal behavior of the algorithm for visualization purposes, which will be described below as well. The visualizer provides a visualization for the algorithms listed below.

# How to run
To run this project, simply clone the repo and run "python3 main.py". We have not created a dependencies file yet (is on our TODO list) so you may need to install all dependencies one by one.

When the project is completely finished, we plan to migrate it over to a python repl application to prevent the need to clone the repo to be able to use the application.

## Algorithms

**Note: For most of these algorithms, the visualization method ends once the target is reached from the source. This is technically not correct for Bellman Ford and Johnson's algorithms, since they calculate the solutions to the single source shortest path problem (source to all vertices) and the all pairs shortest path problem (all vertices to each other) respectively. However, we do run these parts in the background so that when the target (for Bellman Ford) or source/target (for Johnson's) is/are moved, we can easily display the shortest paths instantly. For the other algorithms where we should stop when we reach the target, we go ahead and calculate the shortest path to every target in the background so that the target can be moved around.**


* Depth First Search: 
This is a basic depth first search on this graph, where the order of directions that the graph will be explored in is left, down, right, and up. Note that this algorithm does not guarantee to find the shortest path (on most occasions it won't) since DFS is not really used to find the shortest distance and the shortest path that we display on the screen is simply the path that the search had to take to find the target. This algorithm uses a stack to keep track of the order that the nodes should be explored in. This algorithm works on unweighted graphs.


* Breadth First Search: 
This is also a basic breadth first search algorithm where we explore nodes on a level by level basis (where a level is a certain distance away from the target). BFS guarantees the shortest path. This algorithm uses a queue to keep track of the order that the nodes should be explored in. This algorithm works on unweighted graphs.


* Dijkstra's Algorithm: 
This algorithm utilizes a priority queue to determine which nodes to visit next. Unlike the previous two algorithms, Dijkstra's works on  graphs with positive weights. Dijkstra's inserts all of the neighbors of the node that is currently being visited that have not been visited yet into the priority queue with weights of the node's distance (the sum of all of it's parent node's weights) + the weight of the current node in the weights matrix.

* A*:
A* is an adaption of Dijkstra's algorithm that is useful when you have a fixed target. In this approach, you can use a heuristic to make the search algorithm explore more options that are in the direction that you know the search should be going in. This is done by adding the heuristic to the node's distance + the weight of the current node in the weights matrix. Both of the heuristics chosen are common A* heuristics and are admissible (because they never overestimate the cost of reaching the goal).
  * Manhattan Heuristic: This is also known as taxicab distance and is calculated by doing |target_x_value - node_x_value| + |target_y_value - node_y_value|.

  * Euclidean distance heuristic: This is normal straight line distance and is calculated by doing sqrt((target_x_value - node_x_value)^2 + (target_y_value - node_y_value)^2).
  
* Greedy Best First Search:
This algorithm is almost exactly the same as A*, except for the fact that the weights play no role in the search. The next nodes to explore are directly dictated by the heuristic (this is each node in the priority queue's weight).

* Bellman Ford:
Bellman Ford is an algorithm that is specifically used due to its ability to deal with negative edge weights. The algorithm is able to detect the presence of negative cycles. However, if the negative cycle does not impact the path to the vertex, we have chosen to still display the shortest path that is found. Bellman ford's algorithm is based on the idea that any vertex can at most be V steps away from any other vertex. In our graph, we can actually decrease this criteria to be at most Width+Height, since this is a grid. Because of this, we know that a cycle has been detected if it takes more than Width+Height rounds to reach every vertex.

