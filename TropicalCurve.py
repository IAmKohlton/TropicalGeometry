import Polynomial


class TropicalCurve(object):
    """ Class for the creation and storage of tropical curves in two variables
    """
    def __init__(self, poly):
        assert isinstance(poly, Polynomial.Polynomial)
        assert len(poly.vars) <= 2
        self.poly = poly.simplify()
