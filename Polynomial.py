class Polynomial(object):
    def __init__(self, input=None):
        if input is None:
            self.poly = (None, None, None)
        else:
            assert isinstance(input, int) or isinstance(input, float) or isinstance(input, Polynomial)
            self.poly = input

    def operate(self, input, op):
        assert isinstance(input, int) or isinstance(input, float) or isinstance(input, Polynomial)
        if self.poly == (None, None, None):
            return Polynomial(input=input)
        else:
            newPoly = Polynomial()
            newPoly.poly = (self, op, input)
            return newPoly

    def __add__(self, input):
        return self.operate(input, "+")

    def __radd__(self, input):
        return self.operate(input, "+")

    def __mul__(self, input):
        return self.operate(input, "*")

    def __rmul__(self, input):
        return self.operate(input, "*")

    def __str__(self):
        if self.poly is (None, None, None):
            return ""
        elif not isinstance(self.poly, tuple):
            return str(self.poly)
        else:
            return "(" + str(self.poly[0]) + self.poly[1] + str(self.poly[2]) + ")"
