import Variable
from numpy import prod


def ensurePoly(ob):
    if isinstance(ob, (int, float, Variable.Variable)):
        return Polynomial(ob)
    elif isinstance(ob, Polynomial):
        return ob
    else:
        raise Exception("Tried to convert a non-int, float, variable to a poly")


class Polynomial(object):
    """ A tropical polynomial. This is a polynomial where addition is done with min(), and multiplication is done with +.
    """

    #########################################
    # Contructors and utility functions
    #########################################
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
        elif isinstance(self.poly, list):
            self.vars = input.vars.copy()
        else:
            self.vars = set()

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

    #############################################
    # Public Methods
    #############################################
    def __add__(self, input):
        return self.__operate(input, "+")

    def __radd__(self, input):
        return self.__operate(input, "+")

    def __mul__(self, input):
        return self.__operate(input, "*")

    def __rmul__(self, input):
        return self.__operate(input, "*")

    def __pow__(self, input):
        assert isinstance(input, int)
        return self.__operate(input, "^")

    def isSimple(self):
        return isinstance(self.poly, (int, float, Variable.Variable))

    def eval(self, x):
        """ Evaluate the polynomial when variables are equal to x
            where x is a dict assigning the names of variables to numbers
        """
        if self.poly is None:
            return None

        varNameSet = {y.name for y in self.vars}
        if not isinstance(x, dict):
            if len(self.vars) != 1:
                raise Exception("Tried to evaluate polynomial %s with a single variable, but there is more than one variable that needs to be assigned" % str(self))
        elif varNameSet != set(x.keys()):
            raise Exception("Didn't assign all of the variables in the polynomial")

        return self.__evalRecurse(x)

    def simplify(self):  # TODO too complex, refactor
        """ Simplify the polynomial to sum of monomial form
        """
        simplified = self.__simplifyRecurse()
        # distributed out the polynomial. Now need to collect like terms
        simplified.vars = self.vars.copy()
        orderedVars = sorted(list(self.vars))

        powers = {}  # will have keys of tuples. The tuples will represent the power of a variable. Values will be the
        for monomial in simplified.poly[1:]:
            power = [0] * len(orderedVars)
            total = 0

            if monomial.isSimple():
                monomial.poly = ["*", monomial.poly]

            for term in monomial.poly[1:]:
                term = ensurePoly(term)
                if isinstance(term.poly, (int, float)):
                    total += term.poly
                elif isinstance(term.poly, (Variable.Variable)):
                    power[orderedVars.index(term.poly)] += 1

            power = tuple(power)
            if power not in powers:
                powers[power] = total
            else:
                powers[power] = min(total, powers[power])

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

    #############################################
    # Private Helper Methods
    #############################################
    def __merge(self, inputPoly, op):
        """ Merge two polynomials into one
        """
        newPoly = Polynomial()

        # cast the input to a Polynomial
        inputPoly = ensurePoly(inputPoly)
        if isinstance(inputPoly.poly, (int, float, Variable.Variable)):
            input = Polynomial()
            input.poly = [op, inputPoly.poly]
        else:
            input = inputPoly

        if isinstance(self.poly, (int, float, Variable.Variable)):
            self.poly = [op, self.poly]

        if op == self.poly[0] and op == input.poly[0]:
            newPoly.poly = self.poly + input.poly[1:]
        elif op == self.poly[0]:
            newPoly.poly = self.poly
            newPoly.poly.append(input)
        elif op == input.poly[0]:
            newPoly.poly = [input.poly[0], self]
            newPoly.poly.extend(input.poly[1:])
        else:
            newPoly.poly = [op, self, input]

        return newPoly

    def __operate(self, input, op):
        """ A generalized version of addition, multiplication, and exponentiation
        """
        assert isinstance(input, (int, float, Variable.Variable, Polynomial))

        if self.poly is None:
            return Polynomial(input=input)
        else:
            newPoly = self.__merge(input, op)

            if isinstance(input, Polynomial):
                newPoly.vars = input.vars | self.vars
            elif isinstance(input, Variable.Variable):
                newPoly.vars = {input} | self.vars
            else:
                newPoly.vars = self.vars
            return newPoly

    def __evalRecurse(self, x):
        if isinstance(self.poly, Variable.Variable):
            return x[self.poly.name]
        elif isinstance(self.poly, (int, float)):
            return self.poly
        elif isinstance(self.poly, list):
            # resultList = [branch.__evalRecurse(x) for branch in self.poly[1:]]
            resultList = []
            for branch in self.poly[1:]:
                resultList.append(ensurePoly(branch).__evalRecurse(x))
            if self.poly[0] == "+":
                return min(resultList)
            if self.poly[0] == "*":
                return sum(resultList)
            if self.poly[0] == "^":
                return prod(resultList)

    ###############################################
    # Helper Methods For simplify()
    ###############################################
    def __simplifyRecurse(self):  # TODO make this work with ^
        """ This function relies on the fact that for a given node of a polynomial,
            all of it's children will be the same operation.
            The exponential functions breaks this so we'll deal with it later
        """
        # check if we're a + node, a * node, or a simple node
        if isinstance(self.poly, (int, float, Variable.Variable)):
            return self
        elif self.poly[0] == "+":
            self.__handlePowPlus()

            newPoly = Polynomial()
            newPoly.poly = ["+"]
            for branch in self.poly[1:]:
                simplifiedBranch = ensurePoly(branch).__simplifyRecurse()
                if not simplifiedBranch.isSimple():
                    for additiveTerm in simplifiedBranch.poly[1:]:
                        newPoly.poly.append(additiveTerm)
                else:
                    newPoly.poly.append(simplifiedBranch)
            return newPoly
        elif self.poly[0] == "*":
            self.__handlePowTimes()

            nonSimple, simple = self.__partitionSimpleAndNonSimpleBranches()

            if len(nonSimple) == 0:  # this means our * node gives a monomial!
                return Polynomial(input=self)
            else:
                # do the full distribution
                simplified = self.__distribute(nonSimple, simple)
                newPoly = Polynomial()
                newPoly.poly = ["+"]
                for branch in simplified.poly[1:]:
                    recursive = ensurePoly(branch).__simplifyRecurse()
                    if recursive.poly[0] == "*":
                        newPoly.poly.append(recursive)
                    elif recursive.poly[0] == "+":
                        newPoly.poly.extend(recursive.poly[1:])
                return newPoly

        elif self.poly[0] == "^":
            # this case will only be hit when we have a ^ node as the root
            newPoly = Polynomial()
            newPoly.poly = ["*"]
            for _ in range(self.poly[2]):
                newPoly.poly.append(self.poly[1])

            simp = newPoly.__simplifyRecurse()
            return simp

    def __distribute(self, nonSimple, simple):
        leftmostBranch = nonSimple[0]
        for right in nonSimple[1:]:
            tempLeft = Polynomial()
            tempLeft.poly = ["+"]
            for leftBranch in leftmostBranch.poly[1:]:
                for rightBranch in right.poly[1:]:
                    crossTerm = Polynomial()
                    crossTerm.poly = ["*"]
                    crossTerm = self.__calculateCrossTermPolynomial(rightBranch, crossTerm)
                    crossTerm = self.__calculateCrossTermPolynomial(leftBranch, crossTerm)
                    tempLeft.poly.append(crossTerm)

            leftmostBranch = tempLeft

        # now all the non simple branches are distributed
        # just need to distribute the simple branches
        distributedPoly = Polynomial()
        distributedPoly.poly = ["+"]
        for child in leftmostBranch.poly[1:]:
            distChild = Polynomial()
            distChild.poly = ["*"]
            if ensurePoly(child).isSimple():
                childPoly = Polynomial()
                childPoly.poly = ["*", child]
                child = childPoly
            distChild.poly.extend(child.poly[1:])
            distChild.poly.extend(simple)
            distributedPoly.poly.append(distChild)

        return distributedPoly

    def __calculateCrossTermPolynomial(self, branch, crossTerm):
        branch = ensurePoly(branch)
        if isinstance(branch.poly, (int, float, Variable.Variable)):
            crossTerm.poly.append(branch.poly)
        else:
            for subterm in branch.poly[1:]:
                crossTerm.poly.append(subterm)
        return crossTerm

    def __partitionSimpleAndNonSimpleBranches(self):
        nonSimple = []
        simple = []
        for branch in self.poly[1:]:
            branch = ensurePoly(branch)
            if isinstance(branch.poly, (int, float, Variable.Variable)):
                simple.append(branch.poly)
            else:
                nonSimple.append(branch)

        return nonSimple, simple

    def __handlePowPlus(self):
        newPolyList = ["+"]
        for branch in self.poly[1:]:
            if isinstance(branch, Polynomial) and isinstance(branch.poly, list) and branch.poly[0] == "^":
                powerPoly = Polynomial()
                powerPoly.poly = ["*"]
                productOfPowers = prod(branch.poly[2:])
                for _ in range(productOfPowers):
                    powerPoly.poly.append(branch.poly[1])

                newPolyList.append(powerPoly)
            else:
                newPolyList.append(branch)
        self.poly = newPolyList

    def __handlePowTimes(self):
        newPolyList = ["*"]
        for branch in self.poly[1:]:
            if isinstance(branch, Polynomial) and isinstance(branch.poly, list) and branch.poly[0] == "^":
                powMovedDown = Polynomial()
                powMovedDown.poly = ["+", float("inf"), branch]
                newPolyList.append(powMovedDown)
            else:
                newPolyList.append(branch)
        self.poly = newPolyList
