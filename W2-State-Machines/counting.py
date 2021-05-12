class SM:
    """
    A superclass that contains generally useful methods that apply to all state 
    machines. Any subclass of SM needs a startState attribute and the method 
    getNextValues. 
    """
    def start(self):
        """
        Creates an attribute of the instance state and assigns it to the value
        of the startState attribute from the instance.
        """
        self.state = self.startState
    def step(self, inp):
        """
        Given an input, computes the output, updates the internal state of the
        machine and returns the output value.
        """
        s, o = self.getNextValues(self.state, inp)
        self.state = s
        return o
    def transduce(self, inputs):
        """
        Returns the sequence of output values that results from feeding the 
        elements of the list inputs into the machine in order.
        """
        self.start()
        return [self.step(inp) for inp in inputs]

class CountingStateMachine(SM):
    """
    Special type of state machine whose states are always integers that start at
    0 and increment by 1 on each transition
    """
    def __init__(self):
        self.startState = 0
    def getNextValues(self, state, inp):
        s, o = state + 1, self.getOutput(state, inp)
        return s, o

class CountMod5(CountingStateMachine):
    """Generates output sequences modulo 5"""
    def getOutput(self, state, inp):
        return state % 5

class AlternateZeros(CountingStateMachine):
    """Generates output sequences which alternate between the input and zero"""
    def getOutput(self, state, inp):
        if state % 2 == 0:
            return inp
        else:
            return 0

# Sample output 
list1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
a = CountMod5()
a.transduce(list1)
# [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
b = AlternateZeros()
b.transduce(list1)
# [0, 0, 2, 0, 4, 0, 6, 0, 8, 0]