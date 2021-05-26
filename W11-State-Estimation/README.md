## Week 11 - State Estimation

In Week 11 we learnt how to use the probability framework developed in week 10 to build systems that are robust in the face of uncertainty. We learnt about stochastic state machines and how to use them in state estimation to infer information about a model based on observable properties. Some of these Python scripts were developed in previous weeks, below are descriptions of the scripts I implemented during this week. 

*  stochasticSM.py:
	*  This implements a stochastic state machine class which contains three fundamental components: an initial state distribution, a state transition model and an observation model. 
*  state_estimator.py:
	*  This implements a state estimator class which given a sequence of inputs and observations computes a probability distribution over the hidden states of the system. It does this in two stages first using Bayes rule to compute a belief state and then the law of total probability to compute the final estimation. 