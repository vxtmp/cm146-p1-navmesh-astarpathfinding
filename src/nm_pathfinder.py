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

    path = []
    boxes = {}
    
    """ unit testing """
    test_mesh (mesh)
    
    # grab source and destination points and add to path
    path.append(source_point)
    path.append(destination_point)
    
    # add them to boxes too
    source_box = find_containing_box(source_point, mesh['boxes'])
    destination_box = find_containing_box(destination_point, mesh['boxes'])
    if (source_box):
        boxes[source_box] = 0
    if (destination_box):
        boxes[destination_box] = 0
    

    return path, boxes.keys()

