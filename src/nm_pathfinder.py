from heapq import heappop, heappush
# =============================================================================
# UNIT TEST ===================================================================
# =============================================================================
def test_mesh (mesh):
    for box in mesh['boxes']:
        print (f"Box: {box}")
        
    for box, neighbors in mesh['adj'].items():
        print (f"Box {box} has neighbors: {neighbors}")
        
# =============================================================================
# HELPER FUNCTIONS ============================================================
# =============================================================================
def point_in_box (point, box):
    x1, x2, y1, y2 = box
    x, y = point
    return x1 <= x <= x2 and y1 <= y <= y2

def find_containing_box (point, boxes):
    for box in boxes:
        if point_in_box(point, box):
            return box
        
    return None

def distance (point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def find_closest_point (point1, box2):
    x1, x2, y1, y2 = box2
    x, y = point1
    x = max(x1, min(x, x2)) # clamp point to destination box
    y = max(y1, min(y, y2))
    
    # finds the closest point on the box to the point
    return (x, y)

def append_path (point1, box2, path):
    x, y = find_closest_point(point1, box2)
    path.append((x, y))

# =============================================================================
# SEARCH ALGORITHMS (BSF) =====================================================
# =============================================================================

def breadth_first_search (source_point, destination_point, mesh, path, boxes):
    source_box = find_containing_box(source_point, mesh['boxes'])
    destination_box = find_containing_box(destination_point, mesh['boxes'])
    if (source_box is None) or (destination_box is None):
        print ("Source or destination point not in any box")
        print ("No path found")
        return
    
    root_queue = []
    root_queue.append(source_box)
    
    distance = 0
    boxes = {}
    boxes[source_box] = distance
    
    # breadth first search
    while root_queue:
        current_box = root_queue.pop(0)
        
        if current_box == destination_box:
            break
        
        for neighbor in mesh['adj'][current_box]:
            if neighbor not in boxes:
                boxes[neighbor] = boxes[current_box] + 1
                root_queue.append(neighbor)
    
    # find path from source to destination
    current_box = destination_box 
    path.append(destination_point)
    while current_box != source_box:
        min_neighbor = boxes[current_box]
        x1, x2, y1, y2 = current_box
        for neighbor in mesh['adj'][current_box]:   # find neighbor with min distance.
            if neighbor in boxes and boxes[neighbor] < min_neighbor:
                min_neighbor = boxes[neighbor]
                x1, x2, y1, y2 = neighbor
        if (x1, x2, y1, y2) == current_box:
            print ("No path found")
            return
        current_box = (x1, x2, y1, y2) # update current box to neighbor box.
        # append path using last point added to path
        append_path(path[-1], current_box, path)
        # path.append(((x1 + x2) // 2, (y1 + y2) // 2))
    path.append(source_point)
    
# =============================================================================
# SEARCH ALGORITHMS (DIJKSTRA) ================================================
# =============================================================================

def dijkstra (source_point, destination_point, mesh, path, boxes):
    source_box = find_containing_box(source_point, mesh['boxes'])
    destination_box = find_containing_box(destination_point, mesh['boxes'])
    if (source_box is None) or (destination_box is None):
        print ("Source or destination point not in any box")
        print ("No path found")
        return
    path.append (source_point)
    
    cellPaths = {source_box: [source_point]}          # maps cells to previous points on path
    cellPathCosts = {source_box: 0}       # maps cells to their pathcosts (found so far)
    queue = []
    heappush(queue, (0, source_box))  # maintain a priority queue of cells
    
    while queue:
        priority, current_box = heappop(queue)
        if (current_box not in boxes or boxes[current_box] > priority):
            boxes[current_box] = priority
        if current_box == destination_box:
            path.extend(cellPaths[current_box])
            print ("Destination reached")
            path.append(destination_point)
            return None
        
        # investigate children
        for neighbor in mesh['adj'][current_box]:
            # calculate cost along this path to child
            prev_point = cellPaths[current_box][-1] if cellPaths[current_box] else source_point
            middle_point = find_closest_point(prev_point, neighbor)
            cost_to_neighbor = priority + distance(prev_point, middle_point)
            
            # if unvisited, or if more optimal path for neighbor found (lower cost)
            if neighbor not in cellPathCosts or cost_to_neighbor < cellPathCosts[neighbor]:
                cellPathCosts[neighbor] = cost_to_neighbor            # update the cost
                # add point to cellPaths
                cellPaths[neighbor] = cellPaths[current_box] + [middle_point]
                # push neighbor to priority queue
                heappush(queue, (cost_to_neighbor, neighbor))
                
    print ("No path found")
    return False

# =============================================================================
# SEARCH ALGORITHMS (A*) ================================================
# =============================================================================

# Just doing euclidean distance.
def heuristic (point1, point2):
    return distance (point1, point2)

def aStar (source_point, destination_point, mesh, path, boxes):
    source_box = find_containing_box(source_point, mesh['boxes'])
    destination_box = find_containing_box(destination_point, mesh['boxes'])
    if (source_box is None) or (destination_box is None):
        print ("Source or destination point not in any box")
        print ("No path found")
        return
    path.append (source_point)
    
    cellPaths = {source_box: [source_point]}          # maps cells to previous points on path
    cellPathCosts = {source_box: 0}       # maps cells to their pathcosts (found so far)
    queue = []
    heappush(queue, (0, source_box))  # maintain a priority queue of cells
    
    while queue:
        priority, current_box = heappop(queue)
        if (current_box not in boxes or boxes[current_box] > priority):
            boxes[current_box] = priority
        if current_box == destination_box:
            path.extend(cellPaths[current_box])
            print ("Destination reached")
            path.append(destination_point)
            return None
        
        # investigate children
        for neighbor in mesh['adj'][current_box]:
            # calculate cost along this path to child
            prev_point = cellPaths[current_box][-1] if cellPaths[current_box] else source_point
            middle_point = find_closest_point(prev_point, neighbor)
            cost_to_neighbor = cellPathCosts[current_box] + distance(prev_point, middle_point)
            
            estimated_cost = cost_to_neighbor + heuristic(middle_point, destination_point)
            
            # if unvisited, or if more optimal path for neighbor found (lower cost)
            if neighbor not in cellPathCosts or cost_to_neighbor < cellPathCosts[neighbor]:
                cellPathCosts[neighbor] = cost_to_neighbor          # update the cost
                # add point to cellPaths
                cellPaths[neighbor] = cellPaths[current_box] + [middle_point]
                # push neighbor to priority queue
                heappush(queue, (estimated_cost, neighbor))
                
    print ("No path found")
    return False


# =============================================================================
# SEARCH ALGORITHMS (BIDIRECTIONAL) ===========================================
# =============================================================================

def reversePath (path):
    reversed_path = []
    for i in range(len(path) - 1, -1, -1):
        reversed_path.append(path[i])
    return reversed_path

def bidirectional (source_point, destination_point, mesh, path, boxes):
    source_box = find_containing_box(source_point, mesh['boxes'])
    destination_box = find_containing_box(destination_point, mesh['boxes'])
    if (source_box is None) or (destination_box is None):
        print ("Source or destination point not in any box")
        print ("No path found")
        return
    path.append (source_point)
    
    forwardPaths = {source_box: [source_point]}          # maps cells to previous points on path
    forwardCosts = {source_box: 0}        # maps cells to their pathcosts (found so far)
    backwardPaths = {destination_box: [destination_point]}          # maps cells to previous points on path
    backwardCosts = {destination_box: 0}        # maps cells to their pathcosts (found so far)
    queue = []
    heappush(queue, (0, source_box, 'forward'))  # maintain a priority queue of cells
    heappush(queue, (0, destination_box, 'backward'))  # maintain a priority queue of cells
    
    while queue:
        priority, current_box, direction = heappop(queue)

        currentPaths = {}
        currentCosts = {}
        otherPaths = {}
        
        if direction == 'forward':
            currentPaths = forwardPaths
            currentCosts = forwardCosts
            otherPaths = backwardPaths
            currentSource = source_point
            currentDestination = destination_point
        else: 
            currentPaths = backwardPaths
            currentCosts = backwardCosts
            otherPaths = forwardPaths
            currentSource = destination_point
            currentDestination = source_point

        # if unvisited, add it to the visited boxes for the parent function to draw visited boxes
        if (current_box not in boxes or boxes[current_box] > priority):
            boxes[current_box] = priority
            
        # check if both paths have visited curr box
        if current_box in otherPaths: 
            # found a path
            path.extend(currentPaths[current_box])
            path.extend(reversePath(otherPaths[current_box]))
            print ("Destination reached")
            return None

        # investigate children
        for neighbor in mesh['adj'][current_box]:
            # calculate cost along this path to child
            prev_point = currentPaths[current_box][-1] if currentPaths[current_box] else currentSource
            middle_point = find_closest_point(prev_point, neighbor)
            
            cost_to_neighbor = currentCosts[current_box] + distance(prev_point, middle_point)
            
            estimated_cost = cost_to_neighbor + heuristic(middle_point, currentDestination)
            
            # if unvisited, or if more optimal path for neighbor found (lower cost)
            if neighbor not in currentCosts or cost_to_neighbor < currentCosts[neighbor]:
                currentCosts[neighbor] = cost_to_neighbor          # update the cost
                # add point to cellPaths
                currentPaths[neighbor] = currentPaths[current_box] + [middle_point]
                # push neighbor to priority queue
                heappush(queue, (estimated_cost, neighbor, direction))
    print ("No path found")
    return False
                
# MAIN FUNCTION ==============================================================
def find_path (source_point, destination_point, mesh):

    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:

        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """

    path = [] # list of points
    boxes = {} # dictionary of explored boxes -> distance value
    
    # test_mesh (mesh)
    
    # breadth_first_search (source_point, destination_point, mesh, path, boxes)
    # dijkstra (source_point, destination_point, mesh, path, boxes)
    # aStar (source_point, destination_point, mesh, path, boxes)
    bidirectional (source_point, destination_point, mesh, path, boxes)
    
    return path, boxes.keys()

