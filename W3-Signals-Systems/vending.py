import statemachine as sm

class Vending(sm.SM):
    """A state machine simulating a vending machine"""
    startState = 0
    def getNextValues(self, state, inp):
        if inp == 'quarter':
            return state + 25, (0, False)
        elif inp == 'cancel':
            return 0, (state, False)
        elif inp == 'dispense' and state < 75:
            return state, (0, False)
        else: # state >= 75
            change = state - 75
            return 0, (change, True)


# Sample output
sample = ['dispense', 'quarter', 'quarter', 'quarter', 'quarter','dispense', 
            'quarter', 'cancel', 'dispense']
print(Vending().transduce(sample))

# [(0, False), (0, False), (0, False), (0, False), (0, False), (25, True), 
#      (0, False), (25, False), (0, False)]