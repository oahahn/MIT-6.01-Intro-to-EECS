## Week 12 - Search Algorithms

In Week 12 we were introduced to the idea of search. We learnt that if we know the domain of possible solutions to a problem and know the steps to get from one part of the domain to the other, then we can search the domain until we reach the solution. We also looked how to optimise these algorithms. Some of these Python scripts were developed in previous weeks, below are descriptions of the scripts I implemented during this week. 

*  search.py:
	*  This implements a Search Node class, a Stack class, a Queue class and a method to model Depth First Search or Breadth First Search algorithms with the option to use dynamic programming. There is also a method that integrates this search algorithm into our state machine framework from previous weeks to be used in state-space search problems.
*  searchAlgorithms.py
	*  This uses the classes in search.py to experiment with basic search algorithms that were used to build up the more complex and flexible search method defined in search.py.
*  farmer.py
	*  This uses state machines to solve an example of a search problem involving a farmer, his goat, a wolf, and a load of cabbage, which need to be transported safely across a river.