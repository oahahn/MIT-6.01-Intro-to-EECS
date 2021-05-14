import statemachine as sm

class SumTSM(sm.SM):
    """
    A terminating state machine class whose inputs are numbers, which outputs
    the sum of its inputs so far, and which terminates when the sum is > 100.
    The current input is reflected immediatley in the output at that time step.
    """
    def __init__(self):
        self.startState = 0
    def getNextValues(self, state, inp):
        return state + inp, state + inp # s, o
    def done(self, state):
        # Terminates when sum > 100
        return state > 100

a = SumTSM()
# print(a.transduce([2, 4, 8, 16, 32, 64, 128]))
# Output: [2, 6, 14, 30, 62, 126, 254]

# A terminating state machine instance that repeats SumTSM four times
fourTimes = sm.Repeat(a, 4)

class CountUpTo(sm.SM):
    """
    A terminating state machine class that counts from 1 up to specified number
    and then terminates
    """
    def __init__(self, end):
        self.startState = 0
        self.endState = end
    def getNextValues(self, state, inp):
        return state + 1, state + 1 # s, o
    def done(self, state):
        return state >= self.endState

m = CountUpTo(3)
# Runs machine 20 times or until termination
# print(m.run(n=20))
# [1, 2, 3]

def negateFun(boolean):
    """Takes a Boolean as input and returns the negation of that Boolean"""
    return not boolean

# Creates a state machine out of the function
negate = sm.PureFunction(negateFun)
# print(negate.transduce([True, False]))

# A state machine whose output alternates between True and False for any input 
# sequence; starting with True.
alternating = sm.Feedback(sm.Cascade(sm.Delay(False), negate))
print(alternating.transduce([1, True, False, True, False, True, False]))
# Output: [True, False, True, False, True, False, True]