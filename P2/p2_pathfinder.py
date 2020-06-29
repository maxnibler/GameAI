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

def coordSearch(pt, x1, x2, y1, y2):
    if x1 == x2:
        if pt[1] < y2:
            if pt[1] > y1:
                return x1, pt[1]
            else:
                return x1, y1
        else:
            return x1, y2
        
    if y1 == y2:
        if pt[1] < x2:
            if pt[1] > x1:
                return pt[0], y1
            else:
                return x1, y1
        else:
            return x2, y1
    
    
def boxDist(pt, box1, box2):
    x1 = min(box1[1], box2[1])
    x2 = max(box1[0], box2[0])
    y1 = min(box1[3], box2[3])
    y2 = max(box1[2], box2[2])
    x, y = coordSearch(pt, x1, x2, y1, y2)
    dist = segmentLength(pt[0],x,pt[1],y)
    return dist, (x,y)

def boxInQ(q, box):
    for x in q:
        if x[2] == box:
            return 1
    return 0

def totalDist(sc, prev, distance, point):
    tot = 0
    while point != sc:
        #print(point)
        #print(distance)
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
    for i in range(0,len(mesh['boxes'])):
        cat = mesh['boxes'][i]
        if inBox(cat,source_point):
            scBox = cat
        if inBox(cat, destination_point):
            dstBox = cat
            
    queue = []
    distance = {}
    backDist = {}
    prev = {}
    backPrev = {}
    point = source_point
    bpoint = destination_point
    currBox = scBox
    bBox = dstBox
    B = []
    path = []
    
    heappush(queue, (0, 0, scBox, point, point, True))
    heappush(queue, (0, 0, dstBox, bpoint, bpoint, False))
    while currBox != bBox and len(queue) != 0:
        dist, diff, box, coord, prePt, flag = heappop(queue)
        if flag:
            currBox = box
        else:
            bBox = box
        
        if flag:
            #"""    
            if currBox == bBox:
                path.append((coord, bpoint))
                point = coord
            else:
                point = coord
                #prev[point] = prePt
            if point in prev:
                currentPathDist = totalDist(source_point, prev, distance, point)
                newPathDist = totalDist(source_point, prev, distance, prePt) + diff
                if currentPathDist > newPathDist:
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
                diff, coord = boxDist(point,currBox,adjBox)
                #print(diff)
                dist = segmentLength(coord[0],bpoint[0],coord[1],bpoint[1])
                heappush(queue, (dist, diff, adjBox, coord, point, flag))
        #"""
        else:
            if bBox == currBox:
                path.append((point, coord))
                bpoint = coord
            else:
                bpoint = coord
                #prev[point] = prePt
            if bpoint in prev:
                currentPathDist = totalDist(destination_point, backPrev, backDist, bpoint)
                newPathDist = totalDist(destination_point, backPrev, backDist, prePt) + diff
                if currentPathDist > newPathDist:
                    backDist[bpoint] = diff
                    backPrev[bpoint] = prePt
            else:
                backDist[bpoint] = diff
                backPrev[bpoint] = prePt
            B.append(bBox)
            for i in range(0,len(mesh['adj'][bBox])):
                adjBox = mesh['adj'][bBox][i]
                if boxInQ(queue, adjBox):
                    continue
                if adjBox in B:
                    continue
                diff, c = boxDist(point,bBox,adjBox)
                #print(diff)
                dist = segmentLength(point[0],c[0],point[1],c[1])
                heappush(queue, (dist, diff, adjBox, c, bpoint, flag))
        #"""
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
    #print(backPrev)
    #for i in range(0, 19):
    while bpoint != destination_point:
        path.append((bpoint, backPrev[bpoint]))
        #print(bpoint, destination_point)
        bpoint = backPrev[bpoint]
    #print(mesh['adj'][currBox][closeInd])
    #print(boxes)
    return path, boxes.keys()
    
