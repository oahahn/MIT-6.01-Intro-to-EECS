## Week 5 - Characterizing System Performance

In Week 5 we learnt about poles. More specifically how to find them and what they tell us about the long-term behavior of an LTI system. We built a simple controller and discovered its long-term behavior based on poles. Below are descriptions of the Python scripts I implemented during this week. 

*  systemFunction.py:
	*  Implements a SystemFunction class for representing system functions and determining basic properties of the system, based on its poles.
*  testSystemFunction.py:
	*  A collection of tests for the SystemFunction class and associated methods.
*  wallFollower.py
	*  Constructs a model of the proportional wall-follower system using the
SystemFunction class.
* robotHead.py
	* Implements a model of a system which controls a motor to turn a robot “head”to face a light. The system consists of a light sensor, a motor and a control circuit. Includes methods to find optimal performance based on the dominant pole. 