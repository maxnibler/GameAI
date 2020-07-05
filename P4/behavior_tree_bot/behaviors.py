import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

def fleetApproaching(state, pid):
    myFleets = state.my_fleets()
    for f in myFleets:
        if f.destination_planet == pid:
            return True
    return False
    pass

def unitExcess(state, p, mine):
    enemyAttacks = []
    allyReinforcements = []
    for f in state.enemy_fleets():
        if f.destination_planet == p.ID:
            enemyAttacks.append(f)
    for f in state.my_fleets():
        if f.destination_planet == p.ID:
            allyReinforcements.append(f)
    units = 0
    for e in enemyAttacks:
        units -= e.num_ships
    for a in allyReinforcements:
        units += a.num_ships
    if mine:
        units += p.num_ships
    else:
        units -= p.num_ships
    return units
    pass

def push(queue, pair):
    for i in range(len(queue)):
        if queue[i][0] > pair[0]:
            queue.insert(i,pair)
            return
    queue.append(pair)
    return

def closestSecurePlanet(state, p):
    distanceQueue = []
    for planet in state.my_planets():
        if planet == p:
            continue
        dist = state.distance(p.ID, planet.ID)
        push(distanceQueue, (dist, planet))
    for pair in distanceQueue:
        if unitExcess(state, pair[1], True) >= -1* unitExcess(state, p, True):
            for f in state.my_fleets():
                if f.source_planet == pair[1].ID:
                    continue
                else:
                    return pair[1]
    #-return max(state.my_planets(), key=lambda p: p.num_ships, default=None)

def attackSuccess(state, fromP, toP, size):
    preGrowth = unitExcess(state, toP, False)
    dist = state.distance(fromP.ID, toP.ID)
    rate = toP.growth_rate
    endSize = preGrowth + (dist * rate)
    if size > endSize:
        return True
    return False

def wait(state):
    return True

def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    
    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    size = strongest_planet.num_ships / 2
    if not attackSuccess(state, strongest_planet, weakest_planet, size):
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, size)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def send_reinforcements(state):
    enemyFleet = state.enemy_fleets()
    myFleet = state.my_fleets()
    for f in enemyFleet:
        for p in state.my_planets():
            if f.destination_planet == p.ID:
                unitSize = unitExcess(state, p, True)
                unitSize = unitSize * -1
                if unitSize < 1:
                    continue                    
                closest = closestSecurePlanet(state, p)
                if closest == None:
                    return False
                if closest.num_ships < unitSize:
                    return issue_order(state, closest.ID,\
                                       f.destination_planet, closest.num_ships - 1)
                else:
                    return issue_order(state, closest.ID, f.destination_planet, unitSize)
    return False
    pass

def spread_to_closest_neutral_planet(state):
    myPlanets = state.my_planets()
    neutralPlanets = state.neutral_planets()
    #search all combos of my planets and neutral planets
    #for the closest capturable planet
    distQ = []
    for m in myPlanets:
        for n in neutralPlanets:
            dist = state.distance(m.ID, n.ID)
            push(distQ, (dist, (m, n)))

    for tup in distQ:
        start = tup[1][0]
        end = tup[1][1]
        if unitExcess(state, start, True) > end.num_ships * 2:
            if fleetApproaching(state, end.ID):
                continue
            return issue_order(state, start.ID, end.ID, end.num_ships+1)
    return False

def seize_easy_planet(state):
    myPlanets = state.my_planets()
    neutralPlanets = state.neutral_planets()
    distQ = []
    for m in myPlanets:
        for n in neutralPlanets:
            dist = state.distance(m.ID, n.ID)
            push(distQ, (dist, (m, n)))

    for tup in distQ:
        start = tup[1][0]
        end = tup[1][1]
        if unitExcess(state, start, True) > end.num_ships * 3:
            if fleetApproaching(state, end.ID):
                continue
            return issue_order(state, start.ID, end.ID, end.num_ships * 2)
    return False
    """
    distance = float('inf')
    #search all combos of my planets and neutral planets
    #for the closest capturable planet
    startPlanet = myPlanets[0]
    endPlanet = neutralPlanets[0]
    for m in myPlanets:
        for n in neutralPlanets:
            #mine = myPlanets[m]
            #neut = neutralPlanets[n]
            if state.distance(m.ID, n.ID) < distance:
                if m.num_ships > n.num_ships * 3:
                    if fleetApproaching(state, n.ID):
                        continue
                    if unitExcess(state, m, True) - n.num_ships*2 < 1:
                        continue
                    startPlanet = m
                    endPlanet = n
                    distance = state.distance(m.ID,n.ID)
    if not startPlanet or not endPlanet:
        return False
    return issue_order(state, startPlanet.ID, endPlanet.ID, endPlanet.num_ships * 2)
    """


