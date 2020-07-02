
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log
import random_bot

num_nodes = 500
explore_faction = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    #if  len(node.untried_actions) > 0:
    leaf = expand_leaf(node, board, state)
    return leaf
    pass
    # Hint: return leaf_node


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    action = node.untried_actions[0]
    node.untried_actions.remove(action)
    newState = board.next_state(state, action)
    #print(action)
    child = MCTSNode(parent=node, parent_action=action, action_list=board.legal_actions(newState))
    node.child_nodes[action] = child
    return child
    pass
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    while not board.is_ended(state):
        last_action = random_bot.think(board, state)
        state = board.next_state(state, last_action)
    score = board.points_values(state)
    #print(score)
    return score
    pass


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while True:
        node.visits += 1
        if won:
            node.wins += 1
        if node.parent == None:
            break
        else:
            node = node.parent
    pass

def nodeState(node, state, board):
    if node.parent == None:
        return state
    state = nodeState(node.parent, state, board)
    state = board.next_state(state, node.parent_action)
    return state


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    actions = board.legal_actions(state)
    
    leaves = []
    sampled_game = state
    node = root_node
    flag = False

    for step in range(num_nodes): 
        while len(node.untried_actions) == 0:
            if len(leaves) == 0:
                flag = True
                break
            node = leaves[0]
            leaves.remove(node)
            sampled_game = nodeState(node, state, board)
        if flag:
            break
        # Do MCTS - This is all you!
        leaf = traverse_nodes(node, board, sampled_game, identity_of_bot)
        leaves.append(leaf)

    for leaf in leaves:
        leafState = nodeState(leaf, state, board)
        score = rollout(board, leafState)
        myScore = score[identity_of_bot]
        if (myScore == 1): won = True
        else: won = False
        backpropagate(leaf, won)

    #print(len(root_node.child_nodes))
    bestRatio = -1
    bestAction = actions[0]
    for key in root_node.child_nodes:
        branch = root_node.child_nodes[key]
        #print(branch.wins,"/",branch.visits)
        if bestRatio <= 0 or branch.visits > 1:
            if branch.visits == 0:
                continue
            ratio = branch.wins/branch.visits
            if bestRatio < ratio:
                bestAction = key
                bestRatio = ratio
    #print(bestRatio," ", bestAction)
    
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return bestAction
