"""
Class and some supporting functions for representing and manipulating system
functions. 
"""

import math
import lib601.poly as poly
import lib601.util as util


class SystemFunction:
    """
    Represents a system function as a ratio of polynomials in R

    Attributes: 
        numerator (Polynomial): the numerator of the system function 
        denominator (Polynomial): the denominator of the system function 
    """
    def __init__(self, numeratorPoly, denominatorPoly):
        self.numerator = numeratorPoly
        self.denominator = denominatorPoly
    
    def poles(self):
        """Returns a list of the poles of the system"""
        coeffsZ = self.denominator.coeffs[:]
        # Reverse so the coefficients are in ascending order
        coeffsZ = list(reversed(coeffsZ))
        # Create a polynomial with these coefficients
        polyZ = poly.Polynomial(coeffsZ)
        # The roots of this polynomial are the poles
        return polyZ.roots()

    def poleMagnitudes(self):
        """Returns a list of the magnitudes of the poles of the system"""
        return [abs(pole) for pole in self.poles]

    def dominantPole(self):
        """Returns the pole with the greatest magnitude"""
        return util.argmax(self.poles(), abs)

    def __str__(self):
        return 'SF(' + self.numerator.__str__('R') + \
               '/' + self.denominator.__str__('R') + ')'

    __repr__ = __str__


def Cascade(sf1, sf2):
    """
    Args:
        sf1, sf2: instances of the SystemFunction class

    Returns:
        a new instance of the SystemFunction class that represents the cascade 
        composition of the input systems
    """
    newNumerator = sf1.numerator * sf2.numerator
    newDenominator = sf1.denominator * sf2.denominator
    return SystemFunction(newNumerator, newDenominator)

def FeedbackSubtract(sf1, sf2=None):
    """
    Args:
        sf1, sf2: instances of the SystemFunction class

    Returns:
        a new instance of the SystemFunction class that represents the feedback 
        subtract composition of the input systems
    """
    newNumerator = sf1.numerator * sf2.denominator
    newDenominator = (sf1.numerator * sf2.numerator + 
                      sf1.denominator * sf2.denominator)
    return SystemFunction(newNumerator, newDenominator)

# Real poles sample output
s1 = sf.SystemFunction(poly.Polynomial([1]), poly.Polynomial([0.63, -1.6, 1]))
print(s1)
# SF(1.000/0.630 R**2 + -1.600R + 1.000)
s1.poles()
# [0.90000000000000069, 0.69999999999999951]
s1.poleMagnitudes()
# [0.90000000000000069, 0.69999999999999951]
s1.dominantPole()
# 0.90000000000000069

# Complex poles sample output
s2 = sf.SystemFunction(poly.Polynomial([1]), poly.Polynomial([1.1, -1.9, 1]))
print(s2)
# SF(1.000/1.100 R**2 + -1.900R + 1.000)
s2.poles()
# [(0.94999999999999996+0.44440972086577957j), 
# (0.94999999999999996-0.44440972086577957j)]
s2.poleMagnitudes()
# [1.0488088481701516, 1.0488088481701516]
s2.dominantPole()
# (0.94999999999999996+0.44440972086577957j)