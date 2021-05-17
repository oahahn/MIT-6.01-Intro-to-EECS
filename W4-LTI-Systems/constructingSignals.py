import lib601.poly as poly
import lib601.sig
from lib601.sig import *

"""
1. This signal should be equal to 3.0 for any time t >= 3 and should equal zero
otherwise
"""
# Multiply the unit step signal by 3
s1 = ScaledSignal(StepSignal(), 3)
# Delay this by 3
step1 = Rn(s1, 3)
step1.plot(-5, 5)

"""
2. This signal should be equal to -3.0 for any time t >= 7 and should equal zero
otherwise
"""
# Multiply the unit step signal by -3
s1 = ScaledSignal(StepSignal(), -3)
# Delay this by 7
step2 = Rn(s1, 7)
step2.plot(-10, 10)

"""
3. This signal should be equal to 3.0 for any time 3 <= t <= 6 and should equal
zero otherwise.
"""
# Delay step 1 by 4 so that for t >= 7 the signal = 3.0
s1 = Rn(step1, 4)
# Add this to the constant -3 so that for t <= 6 the signal is -3 otherwise 0
s2 = SummedSignal(s1, ConstantSignal(-3))
# Add this to step 1 so that for 3 <= t <= 6 the signal is 3 and 0 otherwise
stepUpDown = SummedSignal(step1, s2)
stepUpDown.plot(-10, 10)

"""
4. Use the polyR class to construct a signal that has value 1.0 at time 1, value
3.0 at time 3, value 5.0 at time 5 and is 0 everywhere else.
"""
p = poly.Polynomial([5, 0, 3, 0, 1, 0])
stepUpDownPoly = polyR(UnitSampleSignal(), p)
stepUpDownPoly.plot(0, 10)