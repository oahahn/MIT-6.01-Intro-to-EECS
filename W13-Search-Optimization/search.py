import statemachine as sm
import util as util 

class SearchNode:
    """
    A class representing a search node, extended to incorporate costs
    """
    def __init__(self, action, state, parent, actionCost):
        self.state = state
        self.action = action
        self.parent = parent
        if self.parent:
            self.cost = self.parent.cost + actionCost
        else:
            self.cost = actionCost
    
    def path(self):
        """
        Returns a list of pairs (a, s) corresponding to the path starting at the
        top (root) of the tree, going down to this node. It works its way up the
        tree, until it reaches a node whose parent is None.
        e.g. for D: ((None, 'S'), (1, 'B'), (1, 'D'))
        """
        if self.parent == None:
            return [(self.action, self.state)]
        else:
            return self.parent.path() + [(self.action, self.state)]
    
    def inPath(self, s):
        """
        Takes a state, and returns True if the state occurs anywhere in the path
        from the root to the node.
        """
        if s == self.state:
            return True
        elif self.parent == None:
            return False
        else:
            return self.parent.inPath(s)

map1 = {'S' : ['A', 'B'],
        'A' : ['S', 'C', 'D'],
        'B' : ['S', 'D', 'E'],
        'C' : ['A', 'F'],
        'D' : ['A', 'B', 'F', 'H'],
        'E' : ['B', 'H'],
        'F' : ['C', 'D', 'G'],
        'H' : ['D', 'E', 'G'],
        'G' : ['F', 'H']}

def map1successors(s, a):
    """
    A successor function 
    
    Args:
        s: state
        a (int): an action

    Retutns:
        the new state that will result from taking action a in state s
    """
    return map1[s][a]

class Stack:
    """A class representing stacks as lists"""
    def __init__(self):
        self.data = []
    def push(self, item):
        self.data.append(item)
    def pop(self):
        """
        Pops items off of the end of the list, ensuring that the most recent
        items get popped off first.
        """
        return self.data.pop()
    def isEmpty(self):
        return self.data is []

class Queue:
    """A class representing queues as lists"""
    def __init__(self):
        self.data = []
    def push(self, item):
        self.data.append(item)
    def pop(self):
        """
        Pops items off of the front of the list, ensuring that the oldest items
        get popped off first.
        """
        return self.data.pop(0)
    def isEmpty(self):
        return self.data is []

class PQ:
    """
    A class to model a priority queue
    """
    def __init__(self):
        self.data = []
    def push(self, item, cost):
        self.data.append((cost, item))
    def pop(self):
        (index, cost) = util.argmaxIndex(self.data, lambda x: -x[0])
        return self.data.pop(index)[1] # just return the data item
    def isEmpty(self):
        return self.data is []

def search(initialState, goalTest, actions, successor,
            depthFirst = False, DP = True, maxNodes = 10000):
    """
    Models either a Depth First Search or Breadth First Search algorithm with
    the option to use dynamic programming
    """
    if depthFirst:
        agenda = Stack()
    else:
        agenda = Queue()
    startNode = SearchNode(None, initialState, None)
    if goalTest(initialState):
        return startNode.path()
    agenda.push(startNode)
    if DP: visited = {initialState: True}
    count = 1
    while not agenda.isEmpty() and maxNodes > count:
        n = agenda.pop()
        newStates = []
        for a in actions:
            newS = successor(n.state, a)
            newN = SearchNode(a, newS, n)
            if goalTest(newS):
                return newN.path()
            elif newS in newStates:
                pass
            elif ((not DP) and n.inPath(newS)) or \
                (DP and (newS in visited.keys())):
                pass
            else:
                count += 1
            if DP: visited[newS] = True
            newStates.append(newS)
            agenda.push(newN)
    return None

def smSearch(smToSearch, initialState = None, goalTest = None, maxNodes = 10000,
            depthFirst = False, DP = True):
    """
    Uses state machines as a representation of state-space search problems
    """
    if initialState == None:
        initialState = smToSearch.startState
    if goalTest == None:
        goalTest = smToSearch.done
    return search(initialState, goalTest, smToSearch.legalInputs,
                    # Just returns the next state instead of tuple
                    lambda s, a: smToSearch.getNextValues(s, a)[0],
                    maxNodes = maxNodes,
                    depthFirst=depthFirst, DP=DP)

def ucSearch(initialState, goalTest, actions, successor, heuristic):
    """
    A method to implement a Uniform Cost search algorithm. Instead of testing
    for a goal state when we put an element into the agenda, we test for a goal
    state when we take an element out of the agenda to ensure that we actually
    find the shortest path to a goal state.
    """
    startNode = SearchNode(None, initialState, None, 0)
    if goalTest(initialState):
        return startNode.path()
    # The agenda is a priority queue
    agenda = PQ()
    agenda.push(startNode, 0)
    # Integrate dynamic programming; keep track of expanded nodes
    expanded = {}
    while not agenda.isEmpty():
        n = agenda.pop()
        # Don't consider shortest paths we have already found
        if n.state not in expanded.keys():
            expanded[n.state] = True
            if goalTest(n.state):
                return n.path()
            for a in actions:
                (newS, cost) = successor(n.state, a)
                if newS not in expanded.keys():
                    newN = SearchNode(a, newS, n, cost)
                    agenda.push(newN, newN.cost + heuristic(newS))   
    return None

def argmaxIndex(data, func):
    """
    Takes a list of items and a scoring function, and returns a pair consisting
    of the index of the list with the highest scoring item, and the score of
    that item
    """
    costList = [-func(e) for e in data]
    cost = min(costList)
    costIndex = costList.index(cost)
    indicies = [(lambda x: x[1])(e) for e in data]
    index = indicies[costIndex]
    return index, cost 

l = [(5, 0), (8, 1), (3, 2)]
func = lambda x: -x[0]
argmaxIndex(l, func)