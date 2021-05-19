import lib601.sf as sf
import lib601.optimize as optimize
import operator

def delayPlusPropModel(k1, k2):
    """
    Args:
        k1, k2 (int): gains

    Returns:
        An instance of the SystemFunction class that describes the behaviour of 
        the system when the robot has a delay­ plus-proportional controller
    """
    T = 0.1
    V = 0.1
    # Controller
    module1 = sf.Cascade(sd.R(), sf.Gain(k2))
    controller = sf.FeedforwardAdd(sf.Gain(k1), module1)
    # Plant 1
    module1 = sf.Cascade(sf.R(), sf.Gain(T))
    module2 = sf.FeedbackAdd(sf.Gain(1), sf.R())
    plant1 = sf.Cascade(module1, module2)
    # Plant 2
    module1 = sf.Cascade(sf.Gain(V * T), sf.R())
    module2 = sf.FeedbackAdd(sf.Gain(1), sf.R())
    plant2 = sf.Cascade(module1, module2)
    # Combine the three parts
    module1 =  sf.Cascade(controller, sf.Cascade(plant1, plant2))
    sys = sf.FeedbackSubtract(module1)
    return sys

def bestk2(k1, k2Min, k2Max, numSteps):
    """
    Args:
        k1 (int): the given gain value
        k2Min, k2Max (int): a range of values for the argument
        numSteps (int): how many points to test within the range

    Returns:
        (tuple): the value of k2 for which the system converges most quickly, 
        within the range k2Min, k2Max and the value at this point
    """
    func = lambda k2: abs(delayPlusPropModel(k1, k2).dominantPole())
    return optimize.optOverLine(func, k2Min, k2Max, numSteps)

def anglePlusPropModel(k3, k4):
    """
    Takes gains k3 and k4 as input and returns a SystemFunction that describes
    the system with angle-plus­ proportional control
    """
    T = 0.1
    V = 0.1

    # Plant 1 as before
    module1 = sf.Cascade(sf.R(), sf.Gain(T))
    module2 = sf.FeedbackAdd(sf.Gain(1), sf.R())
    plant1 = sf.Cascade(module1, module2)
    # Plant 2 as before
    module1 = sf.Cascade(sf.Gain(V * T), sf.R())
    module2 = sf.FeedbackAdd(sf.Gain(1), sf.R())
    plant2 = sf.Cascade(module1, module2)
    # The complete system
    module1 = sf.FeedbackSubtract(plant1, sf.Gain(k4))
    module2 = sf.Cascade(sf.Gain(k3), module1)
    sys = sf.FeedbackSubtract(sf.Cascade(module2, plant2))
    return sys

def bestk4(k3, k4Min, k4Max, numSteps):
    """
    Args:
        k3 (int): the given gain value
        k4Min, k4Max (int): a range of values for the argument
        numSteps (int): how many points to test within the range

    Returns:
        (tuple): the value of k4 for which the system converges most quickly, 
        within the range k4Min, k4Max and the value at this point
    """
    func = lambda k4: max(anglePlusPropModel(k3, k4).poleMagnitudes())
    return optimize.optOverLine(func, k4Min, k4Max, numSteps)