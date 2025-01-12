def test_mesh (mesh):
    for box in mesh['boxes']:
        print (f"Box: {box}")
        
    for box, neighbors in mesh['adj'].items():
        print (f"Box {box} has neighbors: {neighbors}")
        
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

# WIP
# def find_midpoint (box1, point1, box2, point2, path):
#     x1, x2, y1, y2 = box1
#     x3, x4, y3, y4 = box2
#     # gets the midpoint along the tangent of the two boxes such that the path is shortest
    
#     return (x, y)

def find_closest_point (point1, box2):
    x1, x2, y1, y2 = box2
    x, y = point1
    x = max(x1, min(x, x2)) # clamp point to destination box
    y = max(y1, min(y, y2))
    
    # finds the closest point on the box to the point
    return (x, y)

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
        path.append(((x1 + x2) // 2, (y1 + y2) // 2))
    path.append(source_point)
                

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
    
    breadth_first_search (source_point, destination_point, mesh, path, boxes)
    
    return path, boxes.keys()

