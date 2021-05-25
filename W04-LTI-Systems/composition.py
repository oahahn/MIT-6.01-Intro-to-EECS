import lib601.sm as sm

"""
Use sm.R, sm.Gain, sm.Cascade, sm.FeedbackAdd and sm.FeedbackSubtract to
construct the state machines y(n) = y(n - 1) + x(n)
"""

def accumulator(init):
    """
    Args:
        init (int): the output at time 0

    Returns:
        y: a state machine whose output at time n is the sum of its inputs up to 
        and including time n
    """
    wire = sm.Gain(1)
    yDelay = sm.Delay(init)
    y = sm.FeedbackAdd(wire, yDelay)
    return y

def accumulatorDelay(init):
    """
    Args:
        init (int): the output at time 0

    Returns:
        y: a state machine whose output at time n is the sum of its inputs up to 
        and including time n-1
    """
    xDelay = sm.Delay(0)
    y = sm.Cascade(xDelay, accumulator(init))
    return y

def accumulatorDelayScaled(s, init):
    """
    Args:
        s (int): the scale factor
        init (int): the output at time 0

    Returns:
        y: a state machine whose output at time n is the sum of the scaled 
        inputs (each scaled by s) up to and including time n-1
    """
    xScale = sm.Gain(s)
    y = sm.Cascade(xScale, accumulatorDelay(init))
    return y

def test_accumulator():
    y = accumulator(0)
    print(y.transduce(list(range(10))))


def test_accumulatorDelay():
    y = accumulatorDelay(0)
    print(y.transduce(list(range(10)))


def test_accumulatorDelayScaled():
    y = accumulatorDelayScaled(2, 0)
    print(y.transduce(list(range(10))))


test_accumulator()
test_accumulatorDelay()
test_accumulatorDelayScaled()