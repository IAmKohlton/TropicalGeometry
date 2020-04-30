class Polynomial(object):
    def __init__(self, input=None):
        if input is None:
            self.poly = (None, None, None)
        else:
            assert type(input) == "int" or type(input) == "float" or type(input) == "Polynomial" or type(input) == "Variable"
            self.poly = input

    def operate(self, input, op):
        assert type(input) == "int" or type(input) == "float" or type(input) == "Polynomial" or type(input) == "Variable"
        if self.poly is (None, None, None):
            return Polynomial(input=input)
        else:
            return Polynomial(input=(self.poly, op, input))

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
        elif type(input) != "tuple":
            return str(input)
        else:
            return str(self.poly[0]) + self.poly[1] + str(self.poly[2])
