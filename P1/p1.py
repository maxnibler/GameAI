from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush

def printPath(prev,end):
    path = [end]
    while end in prev:
        end = prev[end]
        #print(end)
        path.append(end)
    
    return path
        
def pathCost(dist,prev,end):
    cost = 0
    p = end
    while dist[p] > 0:
        cost += dist[p]
        p = prev[p]
        #print(cost)
    return cost

def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as
        their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    myQueue = []
    dist = {}
    prev = {}
    cost = 0
    dist[initial_position] = 0
    
    adjacency = adj(graph,initial_position)
    for x in adjacency:
        heappush(myQueue, (x[1], x[1], initial_position, x[0]))
        
    while len(myQueue) != 0:
        cost, diff, start, end = heappop(myQueue)
        #print(start," ",end)
        #print(prev)
        #print(cost)
        cost = dist[start] + diff
        if end in dist:
            if dist[end] > cost:
                dist[end] = cost
                prev[end] = start
        else:
            dist[end] = cost
            prev[end] = start
        if end == destination:
            #print (dist[end])
            return printPath(prev,destination)
            break
        adjacency = adj(graph,end)
        #print(adjacency)
        #print(myQueue)
        for x in adjacency:
            check = 0
            for item in myQueue:
                if item[3] == x[0] and item[2] == end:
                    if item[0] > cost + x[1]:
                        myQueue.remove(item)
                        break
                    else:
                        check = 1
            if check == 1:
                continue
            if x[0] in dist and dist[x[0]] < cost+x[1]:
                continue
            if x[0] in prev:
                continue
            elif end in prev and prev[end] == x[0]:
                continue
            else:
                heappush(myQueue, (cost+x[1], x[1], end, x[0]))
        pass


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their 
        respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    """
    dict = {}
    for space in graph['spaces']:
        distance = 0
        if space not in graph['walls']:
            path = dijkstras_shortest_path(initial_position, space, graph, adj)
            if path is not None:
                # calculate distance, assuming target is actually reachable
                cell1 = heappop(path)
                while len(path) != 0:
                    cell2 = heappop(path)
                    if cell1[0] == cell2[0] or cell1[1] == cell2[1]:
                        #in this case, the cells should be above or next to each other (not diagonal)
                        distance += int(graph['spaces'][cell1]) * 0.5 + int(graph['spaces'][cell2]) * 0.5
                    else:
                        # in this case, the cells should be diagonal
                        distance += int(graph['spaces'][cell1]) * 0.5 * sqrt(2) + int(graph['spaces'][cell2]) * 0.5 * sqrt(2)
                    cell1 = cell2
            dict[space] = distance
    return dict
    """
    myQueue = []
    dist = {}
    prev = {}
    cost = 0
    dist[initial_position] = 0
    
    adjacency = adj(graph,initial_position)
    for x in adjacency:
        heappush(myQueue, (x[1], x[1], initial_position, x[0]))
        
    while len(myQueue) != 0:
        cost, diff, start, end = heappop(myQueue)
        #print(start," ",end)
        #print(prev)
        #print(cost)
        cost = dist[start] + diff
        if end in dist:
            if dist[end] > cost:
                dist[end] = cost
                prev[end] = start
        else:
            dist[end] = cost
            prev[end] = start
        adjacency = adj(graph,end)
        #print(adjacency)
        #print(myQueue)
        for x in adjacency:
            check = 0
            for item in myQueue:
                if item[3] == x[0] and item[2] == end:
                    if item[0] > cost + x[1]:
                        myQueue.remove(item)
                        break
                    else:
                        check = 1
            if check == 1:
                continue
            if x[0] in dist and dist[x[0]] < cost+x[1]:
                continue
            if x[0] in prev:
                continue
            elif end in prev and prev[end] == x[0]:
                continue
            else:
                heappush(myQueue, (cost+x[1], x[1], end, x[0]))
    return dist
    pass


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining 
        it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    adjCells = []
    #print(cell, " ", level['spaces'][cell])
    for i in range(-1,2):
        for j in range(-1,2):
            adj = (cell[0]+i,cell[1]+j)
            if adj in level['walls']:
                continue
            if i == 0 and j == 0:
                continue
            scCost = .5*level['spaces'][cell]
            adjCost = .5*level['spaces'][adj]
            if i != 0 and j != 0:
                scCost = scCost * sqrt(2)
                adjCost = adjCost * sqrt(2)
            cost = adjCost + scCost
            cellCost = (adj, cost)
            adjCells.append(cellCost)
    return adjCells
    pass


def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")

    


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
#DEFAULT EXAMPLE:----------------------------------------------------------------------------
    filename, src_waypoint, dst_waypoint = 'example.txt', 'a','e'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#"BULLET" 4:----------------------------------------------------------------------------------
# Load custom maze ('my_maze.txt') and print distances to all points in 'my_maze_costs.csv'
    filename, src_waypoint = 'my_maze.txt', 'a'
    cost_to_all_cells(filename, src_waypoint, 'my_maze_costs.csv')
	
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#"BULLET" 2:----------------------------------------------------------------------------------
# Find a path from points 'a' to 'd' in 'test_maze.txt' and output to “test_maze_path.txt”
# 'show_level' may need to be modified to print to a file
    filename, src_waypoint, dst_waypoint = 'test_maze.txt', 'a', 'd'
    test_route(filename, src_waypoint, dst_waypoint)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

