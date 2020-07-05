#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn

# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')
    
    create_zone_plan = Sequence(name='Capture territory')
    closest_planet_check = Check(closest_planet_neutral)
    capture_close_planets = Action(spread_to_closest_neutral_planet)
    create_zone_plan.child_nodes = [closest_planet_check, capture_close_planets]
    
    defend_border_plan = Sequence(name='Skirmish for Control')
    border_threat_check = Check(new_enemy_attack)
    reinforce_borders = Action(send_reinforcements)
    defend_border_plan.child_nodes = [border_threat_check, reinforce_borders]
    
    offensive_plan = Sequence(name='Offensive Strategy')
    largest_fleet_check = Check(have_largest_fleet)
    attack = Action(attack_weakest_enemy_planet)
    offensive_plan.child_nodes = [largest_fleet_check, attack]

    spread_plan = Sequence(name='Its free real estate')
    neutral_planet_check = Check(if_neutral_planet_available)
    capture_free_planets = Action(seize_easy_planet)
    spread_plan.child_nodes = [neutral_planet_check, capture_free_planets]

    no_options_plan = Sequence(name='We probably Lost')
    no_planets_check = Check(no_planets_left)
    do_nothing = Action(wait)
    no_options_plan.child_nodes = [no_planets_check, do_nothing]
    
    """
    reallocate_plan = Sequence(name='Put units in strategic positions Strategy')
    available_units_check = Check(can_move_units)
    shift_units = Action(allocate_forwards)
    reallocate_plan.child_nodes = [available_units_check, shift_units]
    """
    root.child_nodes = [no_options_plan, create_zone_plan, defend_border_plan,\
                        offensive_plan, spread_plan, attack.copy()]

    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
