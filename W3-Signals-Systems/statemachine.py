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

    def run(self, n = 10):
        """
        For a machine that doesn't consume input 
        
        Args:
            n (int): number of steps to run
        Returns:
            list of outputs
        """
        if self.endState > n:
            return self.transduce([None] * n)
        else: 
            return self.transduce([None] * self.endState)
            
class Cascade(SM):
    """
    Simulates cascade composition. Takes in two state machines and uses the 
    output of the first as the input to the second. 
    
    Attributes:
        m1 (state machine): first state machine
        m2 (state machine): second state machine
    """
    def __init__(self, sm1, sm2):
        self.m1 = sm1
        self.m2 = sm2
        self.startState = (sm1.startState, sm2.startState)
    def getNextValues(self, state, inp):
        s1, s2 = state
        newS1, o1 = self.m1.getNextValues(s1, inp)
        # The output of sm1 gets fed as input to sm2
        newS2, o2 = self.m2.getNextValues(s2, o1)
        return (newS1, newS2), o2 # s, o

class Delay(SM):
    """Delay state machine, shifts input by one time step"""
    def __init__(self, v0):
        self.startState = v0
    def getNextValues(self, state, inp):
        # Ouput is the old state
        return inp, state # s, o

class Increment(SM):
    startState = 0
    def __init__(self, incr):
        self.incr = incr
    def getNextValues(self, state, inp):
        return state, inp + self.incr # s, o

class Parallel(SM):
    """
    Simulates parallel composition. Takes in two state machines, which both take  
    the same input. The output of the composite machine is the pair of outputs 
    of the individual machines. 

    Attributes:
        m1 (state machine): first state machine
        m2 (state machine): second state machine
    """
    def __init__(self, sm1, sm2):
        self.m1 = sm1
        self.m2 = sm2
        self.startState = sm1.startState, sm2.startState
    def getNextValues(self, state, inp):
        s1, s2 = state 
        newS1, o1 = self.m1.getNextValues(s1, inp)
        newS2, o2 = self.m2.getNextValues(s2, inp)
        return (newS1, newS2), (o1, o2)

class Parallel2(Parallel):
    def getNextValues(self, state, inp):
        s1, s2 = state 
        i1, i2 = inp 
        newS1, o1 = self.m1.getNextValues(s1, i1)
        newS2, o2 = self.m2.getNextValues(s2, i2)
        return (newS1, newS2), (o1, o2)

class ParallelAdd(Parallel):
    def getNextValues(self, state, inp):
        s1, s2 = state
        newS1, o1 = self.m1.getNextValues(s1, inp)
        newS2, o2 = self.m2.getNextValues(s2, inp)
        return (newS1, newS2), o1 + o2

class Feedback(SM):
    """
    Simulates a feedback combinator in which the output of a machine is fed back
    to be the input of the same machine at the next step
    """
    def __init__(self, sm):
        self.m = sm
        self.startState = self.m.startState
    def getNextValues(self, state, inp):
        # The output cannot depend on the input
        ignore, o = self.m.getNextValues(state, 'undefined')
        newS, ignore = self.m.getNextValues(state, o)
        return newS, o

class Feedback2(Feedback):
    """
    Takes a machine with two inputs and one output, and connects the output of
    the machine to the second input, resulting in a machine with one input and
    one output
    """
    def getNextValues(self, state, inp):
        # The output cannot depend on the input
        ignore, o = self.m.getNextValues(state, (inp, 'undefined'))
        newS, ignore = self.m.getNextValues(state, (inp, o))
        return newS, o

class PureFunction(SM):
    startState = None
    def __init__(self, f):
        self.f = f
    def getNextValues(self, state, inp):
        return state, self.f(inp) # s, o

class Repeat(SM):
    def __init__(self, sm, n = None):
        self.sm = sm
        self.startState = 0, self.sm.startState
        self.n = n
    def done(self, state):
        counter, smState = state 
        return counter == self.n 
    def advanceIfDone(self, counter, smState):
        """
        If the process is to be repeated multiple times, this keeps track of how
        many times the process has repeated and resets the start state when one
        cycle has finished
        """
        while self.sm.done(smState) and not self.done((counter, smState)):
            counter += 1
            smState = self.sm.startState
        return counter, smState
    def getNextValues(self, state, inp):
        counter, smState = state 
        smState, o = self.sm.getNextValues(smState, inp)
        # Check to see if the counter needs to be advanced 
        counter, smState = self.advanceIfDone(counter, smState)
        return (counter, smState), o # s, o

import operator 

##  To work in feedback situations we need to propagate 'undefined'
##  through various operations. 

def isDefined(v):
    return not v == 'undefined'
def allDefined(struct):
    if struct == 'undefined':
        return False
    elif isinstance(struct, list) or isinstance(struct, tuple):
        return reduce(operator.and_, [allDefined(x) for x in struct])
    else:
        return True

# Only binary functions for now
def safe(f):
    def safef(a1, a2):
        if allDefined(a1) and allDefined(a2):
            return f(a1, a2)
        else:
            return 'undefined'
    return safef

safeAdd = safe(operator.add)
safeMul = safe(operator.mul)
safeSub = safe(operator.sub)
