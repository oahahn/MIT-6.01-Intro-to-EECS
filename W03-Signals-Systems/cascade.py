import statemachine as sm

class Cascade(sm.SM):
    """
    Simulates cascade composition. Takes in two state machines and uses the 
    output of the first as the input to the second. Returns a new state machine
    which is the composition of the two original state machines. 
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

sm1 = sm.Delay(1)
sm2 = sm.Delay(2)
c = sm.Cascade(sm1, sm2)
print(c.transduce([3, 5, 7, 9]))
# Output: [2, 1, 3, 5]

sm1 = sm.Delay(1)
sm2 = sm.Increment(3)
c = sm.Cascade(sm1, sm2)
print(c.transduce([3, 5, 7, 9]))
# Output: [4, 6, 8, 10]