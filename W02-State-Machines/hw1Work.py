import pdb
import string
import operator

class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return self.opStr + '(' + str(self.left) + ', ' + str(self.right) + ')'
    __repr__ = __str__

class Sum(BinaryOp):
    opStr = 'Sum'

    def eval(self, env):
        # The inputs could be expressions so we need to evaluate them first
        inp1 = self.left.eval(env)
        inp2 = self.right.eval(env)
        # Add these together
        return operator.add(inp1, inp2)

class Prod(BinaryOp):
    opStr = 'Prod'

    def eval(self, env):
        # The inputs could be expressions so we need to evaluate them first
        inp1 = self.left.eval(env)
        inp2 = self.right.eval(env)
        # Multiply these together
        return operator.mul(inp1, inp2)

class Quot(BinaryOp):
    opStr = 'Quot'

    def eval(self, env):
        # The inputs could be expressions so we need to evaluate them first
        inp1 = self.left.eval(env)
        inp2 = self.right.eval(env)
        # Divide the result
        return operator.__truediv__(inp1, inp2)

class Diff(BinaryOp):
    opStr = 'Diff'

    def eval(self, env):
        # The inputs could be expressions so we need to evaluate them first
        inp1 = self.left.eval(env)
        inp2 = self.right.eval(env)
        # Subtract these
        return operator.sub(inp1, inp2)

class Assign(BinaryOp):
    opStr = 'Assign'

    def eval(self, env):
        """
        When assigning an expression to a variable, we need to add the variable 
        as a key to our environment dictionary and associate it with the  
        evaluated expression 
        """
        env[self.left.name] = self.right.eval(env)
        
class Number:
    def __init__(self, val):
        self.value = val
    def __str__(self):
        return 'Num('+str(self.value)+')'
    __repr__ = __str__
    def eval(self, env):
        """Evaluating a number in the console returns the number"""
        return self.value

class Variable:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Var('+self.name+')'
    __repr__ = __str__
    def eval(self, env):
        # Evaluating a variable in the console returns its associated value
        return env[self.name]

# characters that are single-character tokens
seps = ['(', ')', '+', '-', '*', '/', '=']

def tokenize(string):
    """
    Convert strings into a list of tokens
    
    Args:
        string (string): a sequence of characters

    Returns:
        tokenList (list): a list of tokens; words, numbers or special characters
    """
    tokenList = []
    tempWord = ''
    for char in string:
        if char != ' ' and char not in seps:
            tempWord += char
        elif tempWord != '' and char == ' ':
            tokenList.append(tempWord)
            tempWord = ''
        elif tempWord != '' and char in seps:
            tokenList.append(tempWord)
            tempWord = ''
            tokenList.append(char)
        elif char in seps:
            tokenList.append(char)
    if tempWord != '':
        tokenList.append(tempWord)
    return tokenList

def testTokenize():
    print(tokenize('fred '))
    print(tokenize('777 '))
    print(tokenize('777 hi 33 '))
    print(tokenize('**-)('))
    print(tokenize('( hi * ho )'))
    print(tokenize('(fred + george)'))
    print(tokenize('(hi*ho)'))
    print(tokenize('( fred+george )'))

# testTokenize()

# Simple tokenizer tests
'''
Output:
['fred']
['777']
['777', 'hi', '33']
['*', '*', '-', ')', '(']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
'''

def numberTok(token):
    """
    Returns True if token contains only digits

    Args:
        token (string): a token from a list
    """
    for char in token:
        if not char in string.digits: return False
    return True

def variableTok(token):
    """
    Returns True its first character is a letter

    Args:
        token (string): a token from a list
    """
    for char in token:
        if char in string.ascii_letters: return True
    return False

def parse(tokens):
    """
    Returns a syntax tree from a list of tokens. For example, if the input is
    ['(', '2', '+', '5', ')'] then the output is Sum(Num(2.0), Num(5.0))

    Args:
        tokens (list): a list of tokens

    Returns:
        parsedExp: a syntax tree represented as a chain of expressions 
    """
    def parseExp(index):
        """
        Recursive procedure that takes an integer index into the tokens list and
        produces a pair of values.

        Args:
            index (int): index into the tokens list

        Returns:
            a number, variable or simple expression coupled with the next index
        """
        # If a token represents a number, make it into a Number instance and 
        # return that, paired with the next index
        if numberTok(tokens[index]):
            num = Number(float(tokens[index]))
            return num, index + 1
        # If a token represents a variable, make it into a Variable instance and 
        # return that, paired with the next index
        elif variableTok(tokens[index]):
            var = Variable(str(tokens[index]))
            return var, index + 1
        # Otherwise the sequence of tokens starting at index must be an 
        # expression of the form ( expression op expression ) and we want to 
        # deal with this case using recursion 
        else:
            # Extract the left part of the expression which is either a number
            # or variable and the next index
            leftTree, indexPlus2 = parseExp(index + 1)
            # Retrieve the operation
            op = tokens[indexPlus2]
            # Extract the right part of the expression which is either a number
            # or variable and the next index
            rightTree, indexPlus3 = parseExp(indexPlus2 + 1)
            # Return the appropriate type of expression for the syntax tree
            if op == "+":
                return Sum(leftTree, rightTree), indexPlus3 + 1
            elif op == "-":
                return Diff(leftTree, rightTree), indexPlus3 + 1
            elif op == "*":
                return Prod(leftTree, rightTree), indexPlus3 + 1
            elif op == "/":
                return Quot(leftTree, rightTree), indexPlus3 + 1
            elif op == "=":
                return Assign(leftTree, rightTree), indexPlus3 + 1
    
    # Initialise the indexing over the list of tokens
    parsedExp, nextIndex = parseExp(0)
    return parsedExp

# Simple parsing tests

def testParse():
    print(parse(['a']))
    print(parse(['888']))
    print(parse(['(', 'fred', '+', 'george', ')']))
    print(parse(['(', '(', 'a', '*', 'b', ')', '/', '(', 'cee', '-', 'doh', ')' ,')']))
    print(parse(tokenize('((a * b) / (cee - doh))')))
    print(parse(tokenize('(a = (3 * 5))')))

# testParse()

'''
Output:
Var(a)
Num(888.0)
Sum(Var(fred), Var(george))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Assign(Var(a), Prod(Num(3.0), Num(5.0)))
'''

####################################################################
# Test cases for EAGER evaluator
####################################################################

def testEval():
    env = {}
    Assign(Variable('a'), Number(5.0)).eval(env)
    print(Variable('a').eval(env))
    env['b'] = 2.0
    print(Variable('b').eval(env))
    env['c'] = 4.0
    print(Variable('c').eval(env))
    print(Sum(Variable('a'), Variable('b')).eval(env))
    print(Sum(Diff(Variable('a'), Variable('c')), Variable('b')).eval(env))
    Assign(Variable('a'), Sum(Variable('a'), Variable('b'))).eval(env)
    print(Variable('a').eval(env))
    print(env)

# testEval()

'''
Ouput:
5.0
2.0
4.0
7.0
3.0
7.0
{'a': 7.0, 'b': 2.0, 'c': 4.0}
'''

def isNum(thing):
    """
    Returns True if it is a number

    Args:
        thing: any Python entity
    """
    return type(thing) == int or type(thing) == float

def calc():
    """Runs the calculator interactively"""
    env = {}
    while True:
        # prints %, returns user input
        e = input('%')            
        # Breaks the string e into a list of tokens          
        tokenList = tokenize(e)
        # Create a syntax tree from the expression
        syntaxTree = parse(tokenList)
        # Evaluate the result and print
        print(syntaxTree.eval(env))
        print('   env =', env)

def calcTest(exprs):
    """
    Runs calculator on a list of strings in sequence, using the same environment

    Args:
        exprs (list): a list of strings
    """
    env = {}
    for e in exprs:
        # e is the experession e.g. '(2 + 5)'
        print('%', e)          
        # Breaks expresssion into list of tokens e.g. ['(', '2', '+', '5', ')']   
        tokenList = tokenize(e)
        # Create a syntax tree from the expression e.g. Sum(Num(2.0), Num(5.0))
        syntaxTree = parse(tokenList)
        # Evaluate the result and print 
        print(syntaxTree.eval(env))
        print('   env =', env)
        
# Basic calculator test cases (see handout)
testExprs = ['(2 + 5)',
             '(z = 6)',
             'z',
             '(w = (z + 1))',
             'w'
             ]
# calcTest(testExprs)

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

class Tokenizer(SM):
    """Takes a string and turns it into a list of tokens"""
    def __init__(self):
        self.startState = ''
    
    def getNextValues(self, state, inp):
        # True for unbroken character chain
        charChain = inp.isalpha() and self.state.isalpha()
        # True for unbroken number chain
        numChain = inp.isdigit() and self.state.isdigit()
        if charChain or numChain:
            # Add the input to the chain and output ''
            self.state += inp
            return self.state, self.startState
        elif inp == ' ':
            # Reset the chains and output the number or word
            return self.startState, self.state
        else:
            return inp, self.state

def testTokenizer():
    print(Tokenizer().transduce('fred '))
    print(Tokenizer().transduce('777 '))
    print(Tokenizer().transduce('777 hi 33 '))
    print(Tokenizer().transduce('**-)( '))
    print(Tokenizer().transduce('(hi*ho) '))
    print(Tokenizer().transduce('(fred + george) '))

# testTokenizer()

'''
Output:
['', '', '', '', 'fred']
['', '', '', '777']
['', '', '', '777', '', '', 'hi', '', '', '33']
['', '*', '*', '-', ')', '(']
['', '(', '', 'hi', '*', '', 'ho', ')']
['', '(', '', '', '', 'fred', '', '+', '', '', '', '', '', '', 'george', ')']
'''

def tokenize2(inputString):
    """More concise tokenize function using the Tokenizer state machine class"""
    tokens = Tokenizer().transduce(inputString)
    return [token for token in tokens if token != '']

def testTokenize2():
    print(tokenize2('fred '))
    print(tokenize2('777 '))
    print(tokenize2('777 hi 33 '))
    print(tokenize2('**-)( '))
    print(tokenize2('(hi*ho) '))
    print(tokenize2('(fred + george) '))

'''
Output:
['fred']  
['777']
['777', 'hi', '33']
['*', '*', '-', ')', '(']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
'''