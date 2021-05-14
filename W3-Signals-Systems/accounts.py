import statemachine as sm

# Below are two types of bank accounts with different fees and interest

class BA1(sm.SM):
	startState = 0
	def getNextValues(self, state, inp):
		if inp != 0:
			newState = state * 1.02 + inp - 100
		else:
			newState = state * 1.02
		return newState, newState # s, o

class BA2(sm.SM):
	startState = 0
	def getNextValues(self, state, inp):
		newState = state * 1.01 + inp
		return newState, newState # s, o

"""
Maximize machine

Here we want to make a state machine that computes the balances of both types of 
accounts and outputs the maximum of the two balances. 
"""

a1 = BA1()
a2 = BA2()

# Parallel puts two types of accounts in parallel so that they share an input
# and have individual outputs based on this input
p = sm.Parallel(a1, a2)
# Cascading this with a max function creates a new state machine with one input
# and whose output is the max output of the two types of bank account
maxAccount = sm.Cascade(p, sm.PureFunction(max))
print(maxAccount.transduce([1000, 1500, 2000, 500]))
# Ouput: [1000.0, 2510.0, 4535.1, 5080.451]

"""
Investment machine

Here we want to create an investment machine such that any deposit or withdrawal 
whose magnitude is > 3000 goes in the first account and all others in the second 
account. On every step both bank accounts should continue to earn relevant 
interest. The output should be the sum of the balances in the two accounts.  
"""

class Switcher(sm.SM):
	startState = None
	def getNextValues(self, state, inp):
		if abs(inp) > 3000:
			# Feed the input to the first account and pass 0 to the second
			return state, (inp, 0)
		else: 
			# Feed the input to the second account and pass 0 to the first
			return state, (0, inp)

def add(balances):
	return sum(balances)

# Create two different bank account state machines
ba1 = BA1()
ba2 = BA2()
# Compose these bank account classes into a state machine which takes two
# inputs, puts these through the two types of accounts and adds the two outputs
addAccounts = sm.Cascade(sm.Parallel2(ba1, ba2), sm.PureFunction(add))
# Compose this with the Switcher state machine so that the new machine allocates
# the input to the correct account and ouputs the combined sum
switchAccount = sm.Cascade(Switcher(), addAccounts)
print(switchAccount.transduce([1000, 2000, 4000, 8000, -1000, -5000]))
# Output: [1000.0, 3010.0, 6940.1, 14948.501, 14216.76601, 9380.0892701]