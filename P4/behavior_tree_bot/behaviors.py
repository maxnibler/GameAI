import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
#from heapq import heappush heappop

def fleetApproaching(state, pid):
    myFleets = state.my_fleets()
    for f in myFleets:
        if f.destination_planet == pid:
            return True
    return False
    pass

def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


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
    return False

def spread_to_closest_neutral_planet(state):
    myPlanets = state.my_planets()
    neutralPlanets = state.neutral_planets()
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
                if m.num_ships > n.num_ships:
                    if fleetApproaching(state, n.ID):
                        continue
                    startPlanet = m
                    endPlanet = n
                    distance = state.distance(m.ID,n.ID)
    if not startPlanet or not endPlanet:
        return False
    return issue_order(state, startPlanet.ID, endPlanet.ID, endPlanet.num_ships + 1)
