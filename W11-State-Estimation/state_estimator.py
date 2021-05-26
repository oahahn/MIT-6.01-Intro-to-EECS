import distributions as dist
import statemachine as sm
import stochasticSM as ssm

class StateEstimator(sm.SM):
    def __init__(self, model):
        self.model = model
        self.startState = model.startDistribution

    def getNextValues(self, state, inp):
        td = self.model.transitionDistribution
        (observation, i) = inp
        belief = self.efficientBayes(state, observation)
        dSPrime = self.totalProbability(belief, td(i))
        return (dSPrime, dSPrime)

    def efficientBayes(self, state, observation):
        """
        Updates a distribution P(S) given a new observation O = o using Bayesian 
        reasoning: P(S|O) = P(O|S) * P(S) / P(O)

        Args:
            state: an instance of the DDist class representing P(S)
            observation: the observed value e.g. 'perfect'

        Returns:
            the updated distribution based on the observation P(S|O)
        """
        bayes = {}
        states = state.support()
        obs = self.model.observationDistribution
        # for each state, calculate the numerator in Bayes rule
        for s in states:
            # P(O|S) * P(S)
            bayes[s] = obs(s).prob(observation) * state.prob(s)
        # Normalise the values in the bayes dictionary 
        bayes = {k: v / sum(bayes.values()) for k, v in bayes.items()}
        return dist.DDist(bayes) 

    def totalProbability(self, belief, transDist):
        """
        Calculates P(S_{t+1}) using the law of total probability 
        
        Args:
            belief: a distribution representing the current belief 
            transDist: the models transition distribution

        Returns:
            an instance of the DDist class representing P(S_{t+1})
        """
        total = {}
        states = belief.support()
        for s1 in states:
            for s2 in states:
                if s2 not in total.keys():                             
                    total[s2] = belief.prob(s1) * transDist(s1).prob(s2)
                else:
                    total[s2] += belief.prob(s1) * transDist(s1).prob(s2)
        # Normalise the values in the dictionary 
        total = {k: v / sum(total.values()) for k, v in total.items()}
        return dist.DDist(total)

# Test

transitionTable = \
   {'good': dist.DDist({'good' : 0.7, 'bad' : 0.3}),
    'bad' : dist.DDist({'good' : 0.1, 'bad' : 0.9})}
observationTable = \
   {'good': dist.DDist({'perfect' : 0.8, 'smudged' : 0.1, 'black' : 0.1}),
    'bad': dist.DDist({'perfect' : 0.1, 'smudged' : 0.7, 'black' : 0.2})}

copyMachine = \
 ssm.StochasticSM(dist.DDist({'good' : 0.9, 'bad' : 0.1}),
                # Input is irrelevant; same dist no matter what
                lambda i: lambda s: transitionTable[s],
                lambda s: observationTable[s])
obs = [('perfect', 'step'), ('smudged', 'step'), ('perfect', 'step')]

cmse = StateEstimator(copyMachine)

print(cmse.transduce(obs))
# Output
# [DDist(good: 0.6917808219178082, bad: 0.30821917808219174), 
#  DDist(good: 0.24567307692307697, bad: 0.7543269230769231), 
#  DDist(good: 0.5335867067350186, bad: 0.46641329326498143)]