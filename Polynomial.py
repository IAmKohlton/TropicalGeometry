import Variable
import math


class Polynomial(object):
    """ A tropical polynomial. This is a polynomial where addition is done with min(), and multiplication is done with +.
    """

    def __init__(self, input=None):
        """ initialize the polynomial.
        """
        if input is None:
            self.poly = None
            # it will be convention that this is a list [op, x_1, x_2, ...] which will correspond to something like
            # x_1 + x_2 + ... or x_1 * x_2 * ...
        elif isinstance(input, Polynomial):
            if isinstance(input.poly, (int, float, Variable.Variable)):
                self.poly = input.poly
            else:
                self.poly = input.poly[:]
        else:
            assert isinstance(input, (int, float, Variable.Variable))
            self.poly = input

        if isinstance(self.poly, Polynomial):
            raise Exception("Did something bad")
        elif isinstance(self.poly, Variable.Variable):
            self.vars = {self.poly}
        else:
            self.vars = set()

    def operate(self, input, op):
        """ A generalized version of addition, multiplication, and exponentiation
        """
        assert isinstance(input, (int, float, Variable.Variable, Polynomial))

        if self.poly is None:
            return Polynomial(input=input)
        else:
            newPoly = Polynomial()
            # newPoly.poly = (self, op, input)

            # cast the input to a Polynomial
            if isinstance(input, (int, float, Variable.Variable)):
                input = Polynomial(input=input)

            # these first three cases deal with when one of them is a basic type
            if not isinstance(self.poly, list) and not isinstance(input.poly, list):
                newPoly.poly = [op, self, input]
            elif not isinstance(self.poly, list):
                if op == input.poly[0]:
                    newPoly.poly = input.poly + [self]
                else:
                    newPoly.poly = [op, self, input]
            elif not isinstance(input.poly, list):
                if op == self.poly[0]:
                    newPoly.poly = self.poly + [input]
                else:
                    newPoly.poly = [op, self, input]

            # next four cases deal with when both are polynomials already
            elif op == self.poly[0] and op == input.poly[0]:
                newPoly.poly = self.poly + input.poly[1:]
            elif op == self.poly[0]:
                newPoly.poly = self.poly
                newPoly.poly.append(input)
            elif op == input.poly[0]:
                newPoly.poly = input.poly
                newPoly.poly.append(self)
            else:
                newPoly.poly = [op, self, input]

            if isinstance(input, Polynomial):
                newPoly.vars = input.vars | self.vars
            elif isinstance(input, Variable.Variable):
                newPoly.vars = {input} | self.vars
            else:
                newPoly.vars = self.vars
            return newPoly

    def __add__(self, input):
        return self.operate(input, "+")

    def __radd__(self, input):
        return self.operate(input, "+")

    def __mul__(self, input):
        return self.operate(input, "*")

    def __rmul__(self, input):
        return self.operate(input, "*")

    def __pow__(self, input):
        assert isinstance(input, int)
        return self.operate(input, "^")

    def __str__(self):
        if self.poly is None:
            return ""
        elif not isinstance(self.poly, list):
            return str(self.poly)
        else:
            outString = "("
            operation = self.poly[0]
            for term in self.poly[1:]:
                outString += str(term) + operation
            outString = outString[:-1] + ")"
            return outString

    def evalRecurse(self, x):
        if isinstance(self.poly, Variable.Variable):
            return x[self.poly.name]
        elif isinstance(self.poly, int) or isinstance(self.poly, float):
            return self.poly
        elif isinstance(self.poly, list):
            resultList = [branch.evalRecurse(x) for branch in self.poly[1:]]
            if self.poly[0] == "+":
                return min(resultList)
            if self.poly[0] == "*":
                return sum(resultList)
            if self.poly[0] == "^":
                return math.prod(resultList)

    def eval(self, x):
        if self.poly is None:
            return None

        varNameSet = {y.name for y in self.vars}
        if not isinstance(x, dict):
            if len(self.vars) != 1:
                raise Exception("Tried to evaluate polynomial %s with a single variable, but there is more than one variable that needs to be assigned" % str(self))
        elif varNameSet != set(x.keys()):
            raise Exception("Didn't assign all of the variables in the polynomial")
        result = self.evalRecurse(x)
        return result

    def distribute(self, nonSimple, simple):
        left = nonSimple[0]
        for right in nonSimple[1:]:
            tempLeft = Polynomial()
            tempLeft.poly = ["+"]
            for leftBranch in left.poly[1:]:
                for rightBranch in right.poly[1:]:
                    # need to multiply leftBranch, and rightBranch together.
                    # this will be the product of their sub-branches

                    crossTerm = Polynomial()
                    crossTerm.poly = ["*"]
                    if isinstance(rightBranch.poly, (int, float, Variable.Variable)):
                        crossTerm.poly.append(rightBranch.poly)
                    else:
                        for subterm in rightBranch.poly[1:]:
                            crossTerm.poly.append(subterm)

                    if isinstance(leftBranch.poly, (int, float, Variable.Variable)):
                        crossTerm.poly.append(leftBranch.poly)
                    else:
                        for subterm in leftBranch.poly[1:]:
                            crossTerm.poly.append(subterm)

                    tempLeft.poly.append(crossTerm)
            left = tempLeft

        # now all the non simple branches are distributed
        # just need to distribute the simple branches
        for child in left.poly[1:]:
            child.poly.extend(simple)
        return left

    def simplifyRecurse(self):
        """ This function relies on the fact that for a given node of a polynomial,
            all of it's children will be the same operation.
            The exponential functions breaks this so we'll deal with it later
        """
        # check if we're a + node, a * node, or a simple node
        if isinstance(self.poly, (int, float, Variable.Variable)):
            return self
        elif self.poly[0] == "+":
            newPoly = Polynomial()
            newPoly.poly = ["+"]
            for branch in self.poly[1:]:
                newPoly.poly.append(branch.simplifyRecurse())
            return newPoly
        else:  # we are on a * node
            # this is the complicated step
            # start by partitioning branches into simple, and non simple
            nonSimple = []
            simple = []
            for branch in self.poly[1:]:
                if isinstance(branch, (int, float, Variable.Variable)):
                    simple.append(branch)
                else:
                    nonSimple.append(branch)

            if len(nonSimple) == 0:  # this means our * node gives a monomial!
                return Polynomial(input=self)
            else:
                simplified = self.distribute(nonSimple, simple)
                newPoly = Polynomial()
                newPoly.poly = ["+"]
                for branch in simplified.poly[1:]:
                    newPoly.poly.append(branch.simplifyRecurse())
                return newPoly

    def simplify(self):
        simplified = self.simplifyRecurse()
        # distributed out the polynomial. Now need to collect like terms
        simplified.vars = self.vars.copy()
        orderedVars = sorted(list(simplified.vars))

        powers = {}  # will have keys of tuples. The tuples will represent the power of a variable. Values will be the
        for monomial in simplified.poly[1:]:
            power = [0] * len(orderedVars)
            total = 1
            for term in monomial.poly[1:]:
                if isinstance(term, (int, float)):
                    total *= term
                elif isinstance(term, Variable.Variable):
                    power[orderedVars.index(term)] += 1

            power = tuple(power)
            if power not in powers:
                powers[power] = total
            else:
                powers[power] += total

        finalPoly = Polynomial()
        finalPoly.poly = ["+"]
        finalPoly.vars = self.vars.copy()
        for power in sorted(list(powers.keys())):
            monomial = Polynomial()
            monomial.poly = ["*"]
            if powers[power] != 0:
                monomial.poly.append(powers[power])

            for pow, ind in zip(power, range(len(power))):
                if pow == 0:
                    continue
                elif pow == 1:
                    monomial.poly.append(orderedVars[ind])
                else:
                    monomial.poly.append(orderedVars[ind]**pow)
            finalPoly.poly.append(monomial)
        return finalPoly
