import search as search
import statemachine as sm

def depthFirstSearch(initialState, goalTest, actions, successor):
    """Models a Depth First Search algorithm"""
    agenda = search.Stack()
    if goalTest(initialState):
        return [(None, initialState)]
    # Make root node
    rootNode = search.SearchNode(None, initialState, None)
    # Push the initial node onto the agenda
    agenda.push(rootNode)
    # Run until we find a goal state or the agenda is empty
    while not agenda.isEmpty():
        # Pop the node to be expanded off of the agenda
        parent = agenda.pop()
        # Keep track of all of the new states we have reached from this node
        newChildStates = []
        for a in actions(parent.state):
            # Visit the successor states that can be reached via the actions
            newS = successor(parent.state, a)
            newN = search.SearchNode(a, newS, parent) # action, state, parent
            if goalTest(newS):
                return newN.path()
            elif newS in newChildStates:
                """
                Pruning Rule 2: If there are multiple actions that lead from a
                state r to a state s, consider only one of them. If we find
                another way to reach one of those states, we just ignore it.
                """
                pass
            elif parent.inPath(newS):
                """
                Pruning rule 1: Don't consider any path that visits the same
                state twice. This should check to see whether the current state
                already exists on the path to the node we're expanding and, if
                so, it doesn't do anything with it.
                """
                pass
            else:
                newChildStates.append(newS)
                # Push newly visited nodes onto the agenda
                agenda.push(newN)
    return None

# depthFirstSearch('S', lambda x: x == 'F', map1LegalActions, map1successors)
# [(None, 'S'), (1, 'B'), (2, 'E'), (1, 'H'), (2, 'G'), (0, 'F')]

def breadthFirstSearch(initialState, goalTest, actions, successor):
    """Models a Breadth First Search algorithm"""
    agenda = search.Queue()
    if goalTest(initialState):
        return [(None, initialState)]
    # Make root node
    rootNode = search.SearchNode(None, initialState, None)
    # Push the initial node onto the agenda
    agenda.push(rootNode)
    # Run until we find a goal state or the agenda is empty
    while not agenda.isEmpty():
        # Pop the node to be expanded off of the agenda
        parent = agenda.pop()
        # Keep track of all of the new states we have reached from this node
        newChildStates = []
        for a in actions(parent.state):
            # Visit the successor states that can be reached via the actions
            newS = successor(parent.state, a)
            newN = search.SearchNode(a, newS, parent) # action, state, parent
            if goalTest(newS):
                return newN.path()
            elif newS in newChildStates:
                """
                Pruning Rule 2: If there are multiple actions that lead from a
                state r to a state s, consider only one of them. If we find
                another way to reach one of those states, we just ignore it.
                """
                pass
            elif parent.inPath(newS):
                """
                Pruning rule 1: Don't consider any path that visits the same
                state twice. This should check to see whether the current state
                already exists on the path to the node we're expanding and, if
                so, it doesn't do anything with it.
                """
                pass
            else:
                newChildStates.append(newS)
                # Push newly visited nodes onto the agenda
                agenda.push(newN)
    return None

def breadthFirstSearchDP(initialState, goalTest, actions, successor):
    """Models a Breadth First Search algorithm with dynamic programming"""
    agenda = search.Queue()
    if goalTest(initialState):
        return [(None, initialState)]
    # Make root node
    rootNode = search.SearchNode(None, initialState, None)
    # Push the initial node onto the agenda
    agenda.push(rootNode)
    visited = {initialState: True}
    # Run until we find a goal state or the agenda is empty
    while not agenda.isEmpty():
        # Pop the node to be expanded off of the agenda
        parent = agenda.pop()
        for a in actions(parent.state):
            # Visit the successor states that can be reached via the actions
            newS = successor(parent.state, a)
            newN = search.SearchNode(a, newS, parent) # action, state, parent
            if goalTest(newS):
                return newN.path()
            elif newS in visited.keys():
                # Don't add it to the queue because we already have a shortest 
                # path to that node
                pass 
            else:
                visited[newS] = True
                # Push newly visited nodes onto the agenda
                agenda.push(newN)
    return None

class NumberTestSM(sm.SM):
    """
    Takes a derivative of a complex equation by finding a sequence of operations
    that takes you from the starting expression to one that doesn’t contain any
    derivative operations
    """
    startState = 1
    legalInputs = ['x*2', 'x+1', 'x-1', 'x**2', '-x']
    def __init__(self, goal):
        self.goal = goal
    def nextState(self, state, action):
        if action == 'x*2':
            return state*2
        elif action == 'x+1':
            return state+1
        elif action == 'x-1':
            return state-1
        elif action == 'x**2':
            return state**2
        elif action == '-x':
            return -state
    def getNextValues(self, state, action):
        nextState = self.nextState(state, action)
        return (nextState, nextState)
    def done(self, state):
        return state == self.goal

class NumberTestFiniteSM(NumberTestSM):
    def __init__(self, goal, maxVal):
        self.goal = goal
        self.maxVal = maxVal
    def getNextValues(self, state, action):
        nextState = self.nextState(state, action)
        if abs(nextState) < self.maxVal:
            return (nextState, nextState)
        else:
            return (state, state)

search.smSearch(NumberTestSM(10), initialState = 1, depthFirst = False, DP = False)
# [(None, 1), ('x*2', 2), ('x*2', 4), ('x+1', 5), ('x*2', 10)]

search.smSearch(NumberTestSM(10), initialState = 1, depthFirst = False, DP = True) 
# [(None, 1), ('x*2', 2), ('x*2', 4), ('x+1', 5), ('x*2', 10)]