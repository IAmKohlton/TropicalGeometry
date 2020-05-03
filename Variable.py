import Polynomial
from functools import total_ordering


@total_ordering
class Variable(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)

    def __add__(self, other):
        assert isinstance(other, (int, float, Variable, Polynomial.Polynomial))
        return Polynomial.Polynomial(self) + Polynomial.Polynomial(other)

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        assert isinstance(other, (int, float, Variable, Polynomial.Polynomial))
        return Polynomial.Polynomial(self) * Polynomial.Polynomial(other)

    def __rmul__(self, other):
        return self * other

    def __pow__(self, other):
        assert isinstance(other, int)
        return Polynomial.Polynomial(self) ** other
