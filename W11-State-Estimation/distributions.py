"""
Discrete probability distributions
"""

import random
import operator
import copy
from functools import reduce

class DDist:
    """
    Discrete distribution represented as a dictionary.  Can be sparse, in the
    sense that elements that are not explicitly contained in the dictionary are
    assumed to have zero probability.
    """
    def __init__(self, dictionary):
        """ 
        Dictionary whose keys are elements of the domain and values are their
        probabilities. 
        """
        self.d = dictionary

    def dictCopy(self):
        """
        Returns: 
            A copy of the dictionary for this distribution.
        """
        return self.d.copy()

    def prob(self, elt):
        """
        Returns the probability of the given element, elt, in the probability
        distribution. For any element not in the dictionary, probability 0 is 
        returned without error.

        Args:
            elt: an element of the domain of this distribution 
        
        Returns: 
            the probability associated with C{elt}
        """
        if elt in self.d.keys():
            return self.d[elt]
        else:
            return 0

    def support(self):
        """
        Returns: 
            A list (in arbitrary order) of the elements of this distribution
            with non-zero probabability.
        """
        return [k for k in self.d.keys() if self.prob(k) > 0]

    def draw(self):
        r = random.random()
        sum = 0.0
        for val in self.support():
            sum += self.prob(val)
            if r < sum:
                return val

    def __repr__(self):
        if len(self.d.items()) == 0:
            return "Empty DDist"
        else:
            items = self.d.items()
            dictRepr = [str(k) + ": " + str(p) + ", " for (k, p) in items]
            dictRepr = reduce(operator.add, dictRepr)
            return "DDist(" + dictRepr[:-2] + ")"
    __str__ = __repr__

    def marginalizeOut(self, index):
        """
        Marginalizes out the key at a specified index, only a valid function for 
        joint distributions
        
        Args:
            index: the index of the element to be marginalized out of the joint
            distribution; can take on values 0 or 1
        """
        newDict = {}
        aKeys, bKeys = splitTuples(self.d.keys())
        keysList = [aKeys, bKeys]
        newKeys = keysList[index - 1]
        for key in newKeys:
            value = 0
            for jointKey, jointValue in self.d.items():
                if key in jointKey:
                    value += jointValue
            newDict[key] = value 
        return DDist(newDict)

    def conditionOnVar(self, index, value):
        """
        Only valid for joint distributions. Computes P(A|B = b) from a joint
        distribution P(A, B) via Bayes rule: P(A|B = b) = P(A, B) / P(B = b)
        
        Args:
            index: either 0 or 1, specifies which variable to condition on
            value: a value to condition on

        Returns:
            an instance of the DDist class representing P(A|B = b)
        """
        bayes = {}
        aKeys, bKeys = splitTuples(self.d.keys())
        keysList = [aKeys, bKeys]
        newKeys = keysList[index - 1]
        for key in newKeys: 
            numerator = 0
            denominator = 0
            for jointKey, jointValue in self.d.items():
                if value in jointKey:
                    denominator += jointValue
                if (key in jointKey) and (value in jointKey):
                    numerator = jointValue
            bayes[key] = numerator / denominator
        return DDist(bayes)

gradeDist = DDist({'a': 0.3, 'b': 0.3, 'c': 0.3, 'd' : 0.07, 'f' : 0.03})
# DDist(a: 0.3, b: 0.3, c: 0.3, d: 0.07, f: 0.03)

foo = DDist({'hi': 0.6, 'med': 0.1, 'lo': 0.3})
# DDist(hi: 0.6, med: 0.1, lo: 0.3)

def removeElt(items, i):
    """
    Non-destructively remove the element at index i from a list; returns a copy;
    if the result is a list of length 1, just return the element  
    """
    result = items[:i] + items[i+1:]
    if len(result) == 1:
        return result[0]
    else:
        return result

def incrDictEntry(d, k, v):
    """
    If dictionary C{d} has key C{k}, then increment C{d[k]} by C{v}. Else set
    C{d[k] = v}.
    
    Args:
        d: dictionary
        k: legal dictionary key (doesn't have to be in C{d})
        v: numeric value
    """
    if d.has_key(k):
        d[k] += v
    else:
        d[k] = v

def splitTuples(keys):
    """
    Args:
        keys: keys from a joint distribution that are tuples

    Returns:
        aKeys (list): a list of the first elements of the tuples from keys
        bKeys (list): a list of the second elements of the tuples from keys
    """
    aKeys = [] 
    bKeys = [] 
    for key in keys:
        if removeElt(key, 1) not in aKeys:
            aKeys.append(removeElt(key, 1))
        if removeElt(key, 0) not in bKeys:
            bKeys.append(removeElt(key, 0))
    return aKeys, bKeys

# Tests
PAB = DDist({
    ('a1', 'b2'): 0.270000, 
    ('a1', 'b1'): 0.630000, 
    ('a2', 'b2'): 0.080000, 
    ('a2', 'b1'): 0.020000})

PAB.marginalizeOut(0)
# DDist(b1: 0.650000, b2: 0.350000)
PAB.marginalizeOut(1)
# DDist(a1: 0.900000, a2: 0.100000)
PAB.conditionOnVar(1, 'b1')
# DDist(a1: 0.969231, a2: 0.030769)

def DeltaDist(v):
    """
    The delta distribution with all of the probability mass on a single el­ement
    """
    return DDist({v:1.0})

def UniformDist(elts):
    """
    The uniform distribution, which on a discrete set of size n, assigns 
    probability 1/n to each of the elements
    """
    p = 1.0 / len(elts)
    return DDist(dict([(e, p) for e in elts]))

def JDist(PA, PBgA):
    """
    Represents the joint probability distribution for two variables A and B 
    
    Args:
        PA (DDist instance): the probability distribution for A; P(A)
        PBgA (DDist instance): the conditional probability of B given A; P(B|A)

    Returns:
        an instance of the DDist class whose items are tuples of the form (a,b),
        with values that are the corresponding joint probabilities P(B|A) * P(A)
    """
    joint = {}
    dictA = PA.dictCopy()
    for key1, value1 in dictA.items():
        dictBgA = PBgA(key1).dictCopy()
        for key2, value2 in dictBgA.items():
            joint[(key1, key2)] = value1 * value2 
    return DDist(joint)

def bayesEvidence(PBgA, PA, b):
    """
    Updates a distribution P(A) given new information B = b using Bayesian 
    reasoning
    
    Args:
        PBgA: a conditional distribution specifying P(B|A)
        PA: an instance of the DDist class representing P(A)
        b: a value for B, the new information

    Returns:
        an instance of the DDist class representing P(A|B = b)
    """
    return JDist(PA, PBgA).conditionOnVar(1, b)

def totalProbability(PBgA, PA):
    """
    Calculates P(B) using the law of total probability 
    
    Args:
        PBgA: a conditional distribution specifying P(B|A)
        PA: an instance of the DDist class representing P(A)

    Returns:
        an instance of the DDist class representing P(B)
    """
    return JDist(PA, PBgA).marginalizeOut(0)