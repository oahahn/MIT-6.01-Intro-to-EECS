from itertools import zip_longest

class Polynomial:
    """
    A class to represent a polynomial with basic algebraic operations

    Attributes:
        coeffs (list): list of coefficients used to create an instance
    """
    def __init__(self, coefficients):
        self.coeffs = coefficients
    
    def coeff(self, i):
        """Returns the coefficient of the x^i term of the polynomial"""
        return self.coeffs[len(self.coeffs) - 1 - i]

    def getCoeffs(self):
        return self.coeffs[:]

    def __str__(self):
        """Prints a polynomial in common math format"""
        n = len(self.coeffs)
        result = ''
        for index, value in enumerate(self.coeffs):
            if index == n - 1 and value >= 0:
                result += '+ ' + str(value)
            elif index == n - 1 and value < 0:
                result += '- ' + str(abs(value))
            elif index == n - 2 and value >= 0:
                result += '+ ' + str(value) + ' z '
            elif index == n - 2 and value < 0:
                result += '- ' + str(abs(value)) + ' z '
            elif index == 0 and value >= 0:
                result += str(value) + ' z**' + str(n - index - 1) + ' '
            elif index == 0 and value < 0:
                result += ('-' + str(abs(value)) + ' z**' + str(n - index - 1) +
                          ' ')
            elif value >=0:
                result += '+ ' + str(value) + ' z**' + str(n - index - 1) + ' '
            else:
                result += ('- ' + str(abs(value)) + ' z**' + str(n - index - 1) 
                          + ' ')
        return result

    def __add__(self, other):
        """Adds two polynomials"""
        a, b = self.getCoeffs(), other.getCoeffs()
        # Reverse each list to make syntax cleaner
        a.reverse()
        b.reverse()
        # Add lists element-wise padded with zeros if one is longer
        c = [x + y for x, y in zip_longest(a, b, fillvalue=0)]
        c.reverse()
        return Polynomial(c)

    def __mul__(self, other):
        """Multiplies two polynomials"""
        # Create a list of zeros to fill with resulting coefficients
        new_coeffs = (len(self.coeffs) + len(other.coeffs) - 1) * [0]
        for index_a, value_a in enumerate(self.coeffs):
            for index_b, value_b in enumerate(other.coeffs):
                new_coeffs[index_a + index_b] += value_a * value_b
        return Polynomial(new_coeffs)

    def __call__(self, v):
        """Returns the result of evaluating the polynomial when x equals v"""
        a = self.getCoeffs()
        a.reverse() 
        return sum([a[i] * v**i for i in range(len(a))])

    def roots(self):
        l = self.getCoeffs()
        assert (len(l) == 2 or len(l) == 3), 'Order too high to solve for roots'
        if len(l) == 2:
            return [-l[0] / l[1]]
        else:
            a, b, c = l
            d = b**2 - 4 * a * c
            # If the roots are real
            if d >= 0:
                return [(-b - d**0.5) / (2 * a), (-b + d**0.5) / (2 * a)]
            # If the roots are imaginary
            else:
                d = complex(d, 0)
                return [(-b - d**0.5) / (2 * a), (-b + d**0.5) / (2 * a)]
    
    def __repr__(self):
        """Shell should print the string returned by the __str__ method"""
        return str(self)
       
# Sample output
p1 = Polynomial([1, 2, 3])
p1
# z**2 + 2 z + 3
p2 = Polynomial([100, 200])
p1 + p2
# 1 z**2 + 102 z + 203
p1(1)
# 6
p1(-1)
# 2
(p1 + p2)(10)
# 1323
p1 * p1
# 1 z**4 + 4 z**3 + 10 z**2 + 12 z + 9
p1 * p2 * p1
# 100 z**5 + 600 z**4 + 1800 z**3 + 3200 z**2 + 3300 z + 1800
p1.roots()
# [(-1-1.4142135623730951j), (-0.9999999999999999+1.4142135623730951j)]
p2.roots()
# [-0.5]
p3 = Polynomial([3, 2, -1])
p3.roots()
# [-1.0, 0.3333333333333333]
(p1 * p1).roots()
# AssertionError: Order too high to solve for roots