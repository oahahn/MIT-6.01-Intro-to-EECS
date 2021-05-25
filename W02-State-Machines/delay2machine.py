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

class Delay2Machine(SM):
    """
    A non-terminating state machine class that delays its input by two time
    steps; the output at time i is the input at time i-2. 

    Args:
        startState: starting state of the machine
    """
    def __init__(self, val0, val1):
        self.startState = val0, val1
    def getNextValues(self, state, inp):
        """
        Given the current state and input returns a tuple containing both the 
        next state and the ouput.
        """
        input1, input2 = state
        return (input2, inp), input1   

def runTestsDelay():
    print('Test1:', Delay2Machine(100, 10).transduce([1,0,2,0,0,3,0,0,0,4]))
    print('Test2:', Delay2Machine(10, 100).transduce([0,0,0,0,0,0,1]))
    print('Test3:', Delay2Machine(-1, 0).transduce([1,2,-3,1,2,-3]))
    # Test that self.state is not being changed.
    m = Delay2Machine(100, 10)
    m.start()
    [m.getNextValues(m.state, i) for i in [-1,-2,-3,-4,-5,-6]]
    print('Test4:', [m.step(i) for i in [1,0,2,0,0,3,0,0,0,4]])

runTestsDelay()

# Expected results:
#Test1: [100, 10, 1, 0, 2, 0, 0, 3, 0, 0]
#Test2: [10, 100, 0, 0, 0, 0, 0]
#Test3: [-1, 0, 1, 2, -3, 1]
#Test4: [100, 10, 1, 0, 2, 0, 0, 3, 0, 0]