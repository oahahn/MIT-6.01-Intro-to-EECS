import statemachine as sm

class SearchNode:
    """
    A class representing a search node
    """
    def __init__(self, action, state, parent):
        self.state = state
        self.action = action
        self.parent = parent
    
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