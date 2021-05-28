import search as search
import statemachine as sm

# Indices into the state tuple.
(farmer, goat, wolf, cabbage) = range(4)

class FarmerGoatWolfCabbage(sm.SM):
    """
    A class modelling a search problem, involving a Farmer, his Goat, a wolf,
    and a load of Cabbage, which need to be transported safely across a river
    """
    def __init__(self):
        # Everybody starts out on the left
        self.startState = ('L', 'L', 'L', 'L')
        # The goal is to get everybody on the right
        self.goal = ('R', 'R', 'R', 'R')
        self.legalInputs = ['takeNone', 'takeGoat', 'takeWolf', 'takeCabbage'] 

    def farmerTakesItem(self, state, item):
        """
        This method takes an item across the river. The farmer can only fit one
        item on his boat at a time and must always be on the boat himself. 

        Args:
            state (list): representing the current state 
            item (int): the index of the item to take across the river

        Returns:
            nextState (list): the state after the farmer has taken the item
            across the river
        """
        nextState = state
        if state[0] == state[item] == 'L':
            nextState[0] = 'R'
            nextState[item] = 'R'
            return nextState
        elif state[0] == state[item] == 'R':
            nextState[0] = 'L'
            nextState[item] = 'L'
            return nextState
        else:
            raise Exception('Invalid action: Farmer and item on opposite sides')

    def illegalState(self, state):
        """
        If the farmer leaves the goat and cabbage on the same side of the river,
        when he is not present the goat will eat the cabbage. If the farmer
        leaves the goat and the wolf on the same side of the river, when he is
        not present the wolf will eat the goat so we don't allow these actions.
        """
        if state[1] == state[3] != state[0]:
            return True
        elif state[1] == state[2] != state[0]:
            return True
        else: 
            return False

    def getNextValues(self, state, action):
        assert action in self.legalInputs, 'Illegal input'
        nextState = list(state)
        if action == 'takeNone' and state[0] == 'L':
            nextState[0] = 'R'
        elif action == 'takeNone' and state[0] == 'R':
            nextState[0] = 'L'
        elif action == 'takeGoat':
            nextState = self.farmerTakesItem(nextState, 1)
        elif action == 'takeWolf':
            nextState = self.farmerTakesItem(nextState, 2)
        else:
            nextState = self.farmerTakesItem(nextState, 3)
        if self.illegalState(nextState):
            return list(state), list(state)
        else:
            return nextState, nextState

    def done(self, state):
        return state == self.goal

# Testing
sm = FarmerGoatWolfCabbage()
sm.transduce(['takeGoat'])
# [('R', 'R', 'L', 'L')]
sm.transduce(['takeNone','takeGoat'])
# [('L', 'L', 'L', 'L'), ('R', 'R', 'L', 'L')]
sm.transduce(['takeGoat', 'takeNone', 'takeNone'])
# [('R', 'R', 'L', 'L'), ('L', 'R', 'L', 'L'), ('R', 'R', 'L', 'L')]