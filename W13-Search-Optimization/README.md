## Week 13 - Optimizing a Search

In Week 13 we learnt how to systematically use the information we have about the state space we're searching, in order to save us time and space. We discussed uniform cost search, priority queues and heuristics. Some of these Python scripts were developed in previous weeks, below are descriptions of the scripts I implemented during this week. 

*  search.py:
	*  This is slightly modified from last weeks version to incorporate cost in the SearchNode class, a priority queue class, a new Uniform Cost search function with dynamic programming and a heuristic function, which helps to avoid searching paths far away from the goal. 
*  planner.py:
	*  This script implements some functionality that was used in a later lab to allow a robot to make a 2D world map of the obstacles around it and plan a path to a desired destination. It includes a planner method which implements A^* search to find optimal paths for the robot to move among states in the discrete map of the world. It also includes a state machine representing the robot’s dynamics in the grid world.