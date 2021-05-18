import lib601.sf as sf
import lib601.sig as sig
import lib601.ts as ts

#Constants relating to some properties of the motor
k_m = 1000
k_b = 0.5
k_s = 5
# Resistance of the motor
r_m = 20

def controllerAndSensorModel(k_c):
    """
    Args: 
        k_c (float): a gain

    Returns: 
        an instance of the SystemFunction class which represents the
        controller/sensor system with the input gain
    """
    return sf.Cascade(sf.Gain(k_s), sf.Gain(k_c))

def integrator(T):
    """
    Takes as its input the motor’s angular velocity Ωh, and outputs the motor’s 
    angular position Θh

    Args:
        T (int): a timestep, the length of time between samples

    Returns:
        an instance of the SystemFunction class which represents an integrator 
        with the appropriate timestep
    """
    system1 = sf.Cascade(sf.R(), sf.Gain(T))
    system2 = sf.FeedbackAdd(sf.Gain(1), sf.R())
    return sf.Cascade(system1, system2)

def motorModel(T):
    """
    Takes V_c as input and generates Ωh as output through the equation
    sf.Gain((k_m * T) / (k_b * k_m * T + r_m))

    Args:
        T (int): a timestep, the length of time between samples

    Returns:
        an instance of the SystemFunction class which represents a motor
    """
    system1 = sf.Cascade(sf.Gain(k_m/r_m), sf.R())
    system2 = sf.Cascade(sf.Gain(T), sf.FeedbackAdd(sf.Gain(1), sf.R()))
    system3 = sf.Cascade(system1, system2)
    return sf.FeedbackSubtract(system3, sf.Gain(k_b))

def plantModel(T):
    """
    Args: 
        T (int): a timestep, the length of time between samples

    Returns: 
        an instance of the SystemFunction class which represents the entire
        plant
    """
    return sf.Cascade(motorModel(T), integrator(T))

def lightTrackerModel(T, k_c):
    """
    Connects all of these systems together into one large system whose input Θ_l
    is the angular position of the light, and whose output Θh is the angular
    position of the head. 
    
    Args: 
        T (int): a timestep, the length of time between samples
        k_c (float): the gain to use for the controller

    Returns: 
        an instance of the SystemFunction class which represents the entire
        light-tracking system with the specified gains and timesteps
    """
    system = sf.Cascade(controllerAndSensorModel(k_c), plantModel(T))
    return sf.FeedbackSubtract(system)

def plotOutput(sfModel):
    """Plot the output of the given SF, with a unit-step signal as input"""
    smModel = sfModel.differenceEquation().stateMachine()
    outSig = ts.TransducedSignal(sig.StepSignal(), smModel)
    outSig.plot()

# Optimal solutions 

def get_best_k_c(T, k_cmin, k_cmax, numsteps):
    """
    Computes the magnitude of the system’s dominant pole, then finds the value 
    of k that produces the minimum value of this function
    """
    domPole = abs(lightTrackerModel(T, k_c).dominantPole())
    print(optimize.optOverLine(lambda k_c: domPole, k_cmin, k_cmax, numsteps))

get_best_k_c(0.02, -10, 20, 300)