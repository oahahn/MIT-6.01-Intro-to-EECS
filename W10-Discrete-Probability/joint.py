import distributions as dist

def PTgD(Disease):
    """
    A function to model a conditinal distribution

    Args: 
        Disease: either 'disease' or 'noDisease'

    Returns: 
        a probability distribution that represents the distribution of Test,
        conditioned on Disease having the specified value.
    """
    if Disease == 'disease':
        return dist.DDist({'posTest': 0.98, 'negTest': 0.02})
    elif Disease == 'noDisease':
        return dist.DDist({'posTest': 0.05, 'negTest': 0.95})
    else: 
        raise Exception('Invalid value for Disease')
        
PTgD('disease').prob('posTest')
# 0.98

"""Joint distribution of P(Disease, Test)"""

Disease = dist.DDist({'disease': 0.0001, 'noDisease': 0.9999})
# Create the probabilities using P(B|A) * P(A)
p1 = PTgD('noDisease').prob('posTest') * Disease.prob('noDisease')
p2 = PTgD('disease').prob('posTest') * Disease.prob('disease')
p3 = PTgD('noDisease').prob('negTest') * Disease.prob('noDisease')
p4 = PTgD('disease').prob('negTest') * Disease.prob('disease')
joint = dist.DDist({
    ('noDisease', 'posTest') : p1,
    ('disease', 'posTest')   : p2,
    ('noDisease', 'negTest') : p3,
    ('disease', 'negTest')   : p4
})

"""Marginalising Disease out of the joint distribution to create P(Test)"""

# Create the probabilities by summing over values in Disease
p1 = joint.prob(('noDisease', 'posTest')) + joint.prob(('disease', 'posTest'))
p2 = joint.prob(('noDisease', 'negTest')) + joint.prob(('disease', 'negTest'))
marginal = dist.DDist({'posTest': p1, 'negTest': p2})


"""
Creating the distribution P(Disease | Test = 'posTest') using Bayes rule i.e.
P(Test = 'posTest' | Disease) * P(Disease) / P(Test = 'posTest')
"""
p1 = joint.prob(('disease', 'posTest')) / marginal.prob('posTest')
p2 = joint.prob(('noDisease', 'posTest')) / marginal.prob('posTest')
bayes = dist.DDist({'disease': p1, 'noDisease': p2})

"""Creating a joint distribution"""

def PTgD(val):
    """
    Represents the conditional probability distribution P(Test | Disease) 
    
    Args:
        val: a value for Disease

    Returns:
        an instance of the DDist class whose items result from the distribution
        P(Test | Disease = val) 
    """
    if val == 'disease':
        return dist.DDist({'posTest': 0.9, 'negTest': 0.1})
    else:
        return dist.DDist({'posTest': 0.5, 'negTest': 0.5})

disease = dist.DDist({'disease': 0.1, 'noDisease' :0.9})

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
    return dist.DDist(joint)

JDist(disease, PTgD)
# {('disease', 'posTest'): 0.09000000000000001,
#  ('disease', 'negTest'): 0.010000000000000002,
#  ('noDisease', 'posTest'): 0.45,
#  ('noDisease', 'negTest'): 0.45}

# P(A) : disease = dist.DDist({'disease': 0.1, 'noDisease' :0.9})

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

print(bayesEvidence(PTgD, disease, 'posTest'))
# DDist(noDisease: 0.833333, disease: 0.166667)
print(bayesEvidence(PTgD, disease, 'negTest'))
# DDist(noDisease: 0.978261, disease: 0.021739)

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

totalProbability(PTgD, disease)
# DDist(posTest: 0.540000, negTest: 0.460000)