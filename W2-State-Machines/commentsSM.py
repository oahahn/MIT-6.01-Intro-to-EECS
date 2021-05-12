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

class CommentsSM(SM):
    """
    A state machine whose inputs are the characters of a string (representing a
    Python program) and outputs either the input character if it is part of the 
    comment or None if it part of a code section. The two possible states are
    'code' or 'comment'.
    """
    startState = 'code'
    def getNextValues(self, state, inp):
        if state == 'code' and inp != '#':
            return 'code', None
        elif state == 'code' and inp == '#':
            return 'comment', inp
        elif state == 'comment' and inp != '\n':
            return 'comment', inp 
        else:
            return 'code', None

x1 = '''def f(x):  # func
   if x:   # test
     # comment
     return 'foo' '''

x2 = '''#initial comment
def f(x):  # func
   if x:   # test
     # comment
     return 'foo' '''

def runTestsComm():
    m = CommentsSM()
    # Return only the outputs that are not None
    print('Test1:',  [c for c in CommentsSM().transduce(x1) if not c==None])
    print('Test2:',  [c for c in CommentsSM().transduce(x2) if not c==None])
    # Test that self.state is not being changed.
    m = CommentsSM()
    m.start()
    [m.getNextValues(m.state, i) for i in ' #foo #bar']
    print('Test3:', [c for c in [m.step(i) for i in x2] if not c==None])

runTestsComm()

# Expected results:
#Test1: ['#', ' ', 'f', 'u', 'n', 'c', '#', ' ', 't', 'e', 's', 't', '#', ' ', 'c', 'o', 'm', 'm', 'e', 'n', 't']
#Test2: ['#', 'i', 'n', 'i', 't', 'i', 'a', 'l', ' ', 'c', 'o', 'm', 'm', 'e', 'n', 't', '#', ' ', 'f', 'u', 'n', 'c', '#', ' ', 't', 'e', 's', 't', '#', ' ', 'c', 'o', 'm', 'm', 'e', 'n', 't']
#Test3: ['#', 'i', 'n', 'i', 't', 'i', 'a', 'l', ' ', 'c', 'o', 'm', 'm', 'e', 'n', 't', '#', ' ', 'f', 'u', 'n', 'c', '#', ' ', 't', 'e', 's', 't', '#', ' ', 'c', 'o', 'm', 'm', 'e', 'n', 't']