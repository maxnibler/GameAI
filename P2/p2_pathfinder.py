import math
from heapq import heappop, heappush

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
    l = math.sqrt(x*x+y*y)
    return l

def boxCenter(box):
    x = (box[0]+box[1])/2
    y = (box[2]+box[3])/2
    return x,y

def boxDist(pt, box):
    #print(pt)
    #print(box)
    """
    dist = segmentLength(pt[0],box[0],pt[1],box[2])
    newDist = segmentLength(pt[0],box[0],pt[1],box[3])
    if dist > newDist:
        dist = newDist
    newDist = segmentLength(pt[0],box[1],pt[1],box[2])
    if dist > newDist:
        dist = newDist
    newDist = segmentLength(pt[0],box[1],pt[1],box[3])
    if dist > newDist:
        dist = newDist
    """
    x, y = boxCenter(box)
    dist = segmentLength(pt[0],x,pt[1],y)
    return dist

def boxInQ(q, box):
    for x in q:
        if x[2] == box:
            return 1
    return 0

def totalDist(sc, prev, distance, point):
    tot = 0
    #print(prev)
    #print(distance)
    while point != sc:
        #print(tot," ",point)
        #print(distance[point])
        tot += distance[point]
        point = prev[point]
    return tot

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
            
    queue = []
    distance = {}
    prev = {}
    point = source_point
    currBox = scBox
    B = [scBox]
    #print(B)
    path = []
    count = 0
    for i in range(0,len(mesh['adj'][currBox])):
        box = mesh['adj'][currBox][i]
        diff = boxDist(point,box)
        distance[boxCenter(box)] = diff
        heappush(queue, (diff, diff, box, point))
        count += 1
    while currBox != dstBox and len(queue) != 0:
        #print(queue)
        dist, diff, currBox, prePt = heappop(queue)
        #print(currBox,": ", dstBox)
        if currBox == dstBox:
            point = destination_point
        else:
            point = boxCenter(currBox)
        prev[point] = prePt
        if point in distance:
            if distance[point] > diff:
                distance[point] = diff
                prev[point] = prePt
        else:
            distance[point] = diff
            prev[point] = prePt
        B.append(currBox)
        for i in range(0,len(mesh['adj'][currBox])):
            adjBox = mesh['adj'][currBox][i]
            if boxInQ(queue, adjBox):
                continue
            if adjBox in B:
                continue
            diff = boxDist(point,adjBox)
            dist = totalDist(source_point, prev, distance, point) + diff
            heappush(queue, (dist, diff, adjBox, point))
            count += 1
    
    
    boxes = {}
    for box in B:
        boxes[box] = mesh['adj'][box]
        
    if dstBox not in B:
        print("No path!")
        return path, boxes.keys()
    
    while point != source_point:
        path.append((prev[point],point))
        #print(point," ",prev[point])
        point = prev[point]
    #print(mesh['adj'][currBox][closeInd])
    #print(boxes)
    return path, boxes.keys()
