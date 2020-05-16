import Polynomial


class TropicalCurve(object):
    """ Class for the creation and storage of tropical curves in two variables
    """
    def __init__(self, poly):
        if not isinstance(poly, Polynomial.Polynomial):
            raise TypeError("input is not of type Polynomial")
        if len(poly.vars) != 2:
            raise ValueError("input polynomial did not have exactly two distinct variables")
        self.poly = poly.simplify()
