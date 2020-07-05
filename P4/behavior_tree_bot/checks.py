
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

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())
    pass

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
    pass

def no_planets_left(state):
    return not any(state.my_planets())

def new_enemy_attack(state):
    if not any(state.enemy_fleets()):
        return False
    enemyFleet = state.enemy_fleets()
    myFleet = state.my_fleets()
    for f in enemyFleet:
        for p in state.my_planets():
            if f.destination_planet == p.ID:
                return True
                """
                defended = False
                for mf in myFleet:
                    if f.destination_planet == mf.destination_planet:
                        defended = True
                    if not defended:
                        return True
                """
    return False
    pass
