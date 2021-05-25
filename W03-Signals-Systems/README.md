## Week 3 - Signals and Systems

Week 3 introduced the concept of signals and systems. We learnt how signals can be produced through linear combinations of other signals and how to represent systems as block diagrams. We also applied our knowledge from previous weeks to think about systems as state machines and make long-term generalisations with these. Below are descriptions of the Python scripts I implemented during this week. 

*  cascade.py:
	*  In cascade composition, we take two machines and use the output of the first one as the input to the second. The result is a new composite machine which can be act as a new unit. This script implements a basic cascade class to simulate this behaviour. 
*  statemachine.py
	*  A collection of all the useful state machine classes that were frequently used to combine and act on other state machines. 
*  accounts.py
	*  Uses the state machine combinators from statemachine.py to create new more complex state machines from basic building blocks. More specifically basic bank account machines are composed to create a maximise machine and an investment machine. 
*  sequential.py
	*  A few examples of terminating state machine classes that draw on results from previous exercises. 
*  vending.py
	*  A state machine which mimicks a vending machine.