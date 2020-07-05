

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
