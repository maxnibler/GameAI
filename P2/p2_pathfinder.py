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
    path = []
    boxes = {scBox:mesh['adj'][scBox],dstBox:mesh['adj'][dstBox]}
    print(boxes)
    return path, boxes.keys()
