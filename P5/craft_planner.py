import json
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time
from heapq import heappush, heappop

Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])


class State(OrderedDict):
    """ This class is a thin wrapper around an OrderedDict, which is simply a dictionary which keeps the order in
        which elements are added (for consistent key-value pair comparisons). Here, we have provided functionality
        for hashing, should you need to use a state as a key in another dictionary, e.g. distance[state] = 5. By
        default, dictionaries are not hashable. Additionally, when the state is converted to a string, it removes
        all items with quantity 0.

        Use of this state representation is optional, should you prefer another.
    """

    def __key(self):
        return tuple(self.items())

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.__key() < other.__key()

    def copy(self):
        new_state = State()
        new_state.update(self)
        return new_state

    def __str__(self):
        return str(dict(item for item in self.items() if item[1] > 0))


def make_checker(rule):
    # Implement a function that returns a function to determine whether a state meets a
    # rule's requirements. This code runs once, when the rules are constructed before
    # the search is attempted.
    Con = {}
    Req = {}
    if 'Requires' in rule:
        Req = rule['Requires']
    if 'Consumes' in rule:
        Con = rule['Consumes']

    def check(state):
        # This code is called by graph(state) and runs millions of times.
        # Tip: Do something with rule['Consumes'] and rule['Requires'].
        for c in Con:
            if c in state:
                if Con[c] <= state[c]:
                    continue
                else:
                    return False
            else:
                return False
        for r in Req:
            if r in state:
                if state[r] > 0:
                    continue
                else:
                    return False
        return True
    return check


def make_effector(rule):
    # Implement a function that returns a function which transitions from state to
    # new_state given the rule. This code runs once, when the rules are constructed
    # before the search is attempted.
    Con = {}
    #print(rule['Produces'])
    Prod = rule['Produces']
    if 'Consumes' in rule:
        #print(rule['Consumes'])
        Con = rule['Consumes']
    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].
        next_state = state.copy()
        for p in Prod:
            next_state[p] += Prod[p]
        for c in Con:
            next_state[c] -= Con[c]
        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.
    for g in goal:
        print(g,': ',goal[g])
    def is_goal(state):
        # This code is used in the search process and may be called millions of times.
        for g in goal:
            if state[g] < goal[g]:
                return False
        return True

    return is_goal


def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


def heuristic(state):
    # Implement your heuristic here!
    base = 100
    for name, rec in Crafting['Recipes'].items():
        for p in rec['Produces']:
            if p in needs:
                if state[p] > needs[p]:
                    base += state[p]
                else:
                    base -= state[p]
    #print (base)
    return base

def search(graph, state, is_goal, limit, heuristic):

    start_time = time()

    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state

    queue = []
    path = []
    came_from = {}
    state_action = {}
    cost_so_far = {}
    came_from[state] = None
    cost_so_far[state] = 0
    time_cost = {}

    heappush(queue, (0, state))

    while time() - start_time < limit:
        if queue:
            cost, current = heappop(queue)

            if is_goal(current):
                print('success')
                path.append((current, None))
                current = came_from[current]
                while current is not None:
                    path.insert(0, (current, state_action[current]))
                    current = came_from[current]
                # print(path)
                print(time() - start_time, 'seconds.')
                return path
                break
            for recipe in graph(current):
                new_cost = cost_so_far[current] + cost

                if recipe[1] not in cost_so_far or new_cost < cost_so_far[recipe[1]]:
                    cost_so_far[recipe[1]] = new_cost
                    priority = new_cost + heuristic(recipe[1])
                    heappush(queue, (priority, recipe[1]))
                    came_from[recipe[1]] = current
                    state_action[current] = recipe
    # Failed to find a path
    print(time() - start_time, 'seconds.')
    print("Failed to find a path from", state, 'within time limit.')
    return None

if __name__ == '__main__':
    with open('crafting.json') as f:
        Crafting = json.load(f)

    # # List of items that can be in your inventory:
    # print('All items:', Crafting['Items'])
    #
    # # List of items in your initial inventory with amounts:
    # print('Initial inventory:', Crafting['Initial'])
    #
    # # List of items needed to be in your inventory at the end of the plan:
    # print('Goal:',Crafting['Goal'])
    #
    # # Dict of crafting recipes (each is a dict):
    # print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

    # Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)
        
    needs = {}
    for name, rec in Crafting['Recipes'].items():
        if 'Consumes' in rec:
            for c in rec['Consumes']:
                if c in needs:
                    if needs[c] < rec['Consumes'][c]:
                        needs[c] = rec['Consumes'][c]
                else:
                    needs[c] = rec['Consumes'][c]
        if 'Requires' in rec:
            for r in rec['Requires']:
                if r in needs:
                    if needs[r] < rec['Requires'][r]:
                        needs[r] = 1
                else:
                    needs[r] = 1
    #print(needs)

    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])

    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])

    # Search for a solution
    resulting_plan = search(graph, state, is_goal, 5, heuristic)

    if resulting_plan:
        # Print resulting plan
        for state, action in resulting_plan:
            print('\t',state)
            print(action)
