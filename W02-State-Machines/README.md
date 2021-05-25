## Week 2 - State Machines

Week 2 introduced the concept of state machines. We discussed particular situations in which thinking of certain problems as state machines have advantages over traditional functional programming approaches. For example, when modelling a system over time where data accumulates or its evolution is important. Below are descriptions of the Python scripts I implemented during this week. 

*  hw1Work.py:
	*  This script implements a simple symbolic calculator that reads, evaluates, and prints arithmetic expres­sions that contain variables as well as numeric values. It is similar, in structure and operation, to the Python interpreter. The calculator operates in two phases. It
		*  Parses the input string of characters to generate a syntax tree; and then
		*  Evaluates the syntax tree to generate a value, if possible, and does any required assignments.
*  delay2machine.py:
	*  A non-terminating state machine class that delays its input by two time steps. This class inherits behaviour from a general state machine superclass. 
*  commentsSM.py
	*  Implements a state machine whose inputs are the characters of a string (representing Python program) and outputs either the input character if it is part of the comment or None if it part of a code section.
*  hammock.py
	*  Includes a class that keeps track of who is allowed to sit on a hammock. This is modelled as state machine. There are some rules as to who is allowed at what time to sit on the hammock.  
*  counting.py
	*  Implements a special type of state machine whose states are always integers that start at 0 and increment by 1 on each transition. Two child classes are created to demonstrate inheritance with state machines. 
*  accounts.py
	*  Includes a class that represents a bank account and a child class in a different currency to demonstrate inheritance. 