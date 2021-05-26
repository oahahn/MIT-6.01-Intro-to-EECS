import statemachine as sm
import distributions as dist

class StochasticSM(sm.SM):
    """Models a stochastic state machine"""
    def __init__(self, startDistribution, transitionDistribution,
                    observationDistribution):
        self.startDistribution = startDistribution
        self.transitionDistribution = transitionDistribution
        self.observationDistribution = observationDistribution

    def startState(self):
        return self.startDistribution.draw()

    def getNextValues(self, state, inp):
        return (self.transitionDistribution(inp)(state).draw(),
                self.observationDistribution(state).draw())


"""Copy machine example"""

# 1. Initial state distribution
initialStateDistribution = dist.DDist({'good': 0.9, 'bad': 0.1})
# 2. Observation model
def observationModel(s):
    if s == 'good':
        return dist.DDist({'perfect': 0.8, 'smudged': 0.1, 'black': 0.1})
    else:
        return dist.DDist({'perfect': 0.1, 'smudged': 0.7, 'black': 0.2})
# 3. State transition model
def transitionModel(i):
    # i is the input at t
    def transitionGivenI(oldState):
        # oldState is S_t
        if oldState == 'good':
            return dist.DDist({'good': 0.7, 'bad': 0.3})
        else:
            return dist.DDist({'good': 0.1, 'bad': 0.9})
    return transitionGivenI

copyMachine = StochasticSM(initialStateDistribution, transitionModel, 
                                observationModel)
copyMachine.transduce(['copy']* 20)