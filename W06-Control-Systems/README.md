## Week 6 - Designing Control Systems

In Week 6 we modelled complex systems by breaking them down into smaller systems and combining them. We also solved for the poles of those complex systems and used them to predict long-term behavior. We then looked at a plot of poles in our system to discover how changing parameters of a small part of a complex system affects the overall behavior of that system. Below are descriptions of the Python scripts I implemented during this week. 

*  remember.py:
	*  Includes a model that analyzes the behavior of whole system when the robot has a delay-plus-proportional controller. The controller depends on the previous distance to the wall as well as the current one and uses this model to find the best gains. 
*  delay.py:
	*  This implements a brain for the delay-plus-proportional controller through two parts in cascade. First sensor input is read and a perpendicular distance is from the wall is calculated. Then using this distance the robot is sent an action. 
*  angle.py:
	*   This implements a brain for the angle-plus-proportional controller in two parts in cascade. First sensor input is read and a perpendicular distance is from the wall on the right and the angle to the wall is calculated. Then using these two pieces of information the robot is sent an action. 