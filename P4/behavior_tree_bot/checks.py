

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def closest_planet_neutral(state):
    if not any(state.neutral_planets()):
        return False
    dist = float('inf')
    for m in state.my_planets():
        for p in state.neutral_planets():
            if dist > state.distance(m.ID, p.ID):
                dist = state.distance(m.ID, p.ID)
    for m in state.my_planets():
        for e in state.enemy_planets():
            if dist > state.distance(m.ID, e.ID):
                return False
    return True

        
    """
    dist = float('inf')
    myPlanets = state.my_planets()
    neutralPlanets = state.neutral_planets()
    enemyPlanets = state.enemy_planets()
    flag = True
    for mine in myPlanets:
        for neut in neutralPlanets:
            if distance(mine, neut) < dist:
                dist = distance(mine, neut)
    for mine in myPlanets:
        for enemy in enemyPlanets:
            if distance(mine, enemy) < dist:
                flag = False
    """
