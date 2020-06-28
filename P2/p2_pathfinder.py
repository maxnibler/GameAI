def swap(a, b):
    temp = a
    a = b
    b = temp
    return a, b

def inBox(box, coor):
    if box[0] > coor[0]:
        return 0
    if box[1] < coor[0]:
        return 0
    if box[2] > coor[1]:
        return 0
    if box[3] < coor[1]:
        return 0
    return 1
    
def segmentLength(x1, x2, y1, y2):
    if x1 > x2:
        x1, x2 = swap(x1, x2)
    if y1 > y2:
        y1, y2 = swap(y1, y2)
    y = y2 - y1
    x = x2 - x1
    l = sqrt(x*x+y*y)
    return l

def find_path (source_point, destination_point, mesh):
    """    Searches for a path from source_point to destination_point through the mesh
    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to
    Returns:
        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """
    #print (source_point)
    #print (destination_point)
    #print (mesh[source_point])
    for i in range(0,len(mesh['boxes'])):
        cat = mesh['boxes'][i]
        if inBox(cat,source_point):
            scBox = cat
        if inBox(cat, destination_point):
            dstBox = cat
    B = [scBox,dstBox]
    print(segmentLength(4,1,5,2))
    path = [(source_point,destination_point)]
    boxes = {}
    for box in B:
        boxes[box] = mesh['adj'][box]
    #print(boxes)
    return path, boxes.keys()
