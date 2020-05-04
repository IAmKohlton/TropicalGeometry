from Polynomial import Polynomial
from Variable import Variable
from random import random
from random import randint
from random import choice


def comparePoly(expected, got):
    """ Compare if two polynomials are equal based on what they evaluate to
        This is a rather crude way of doing but it works in most cases.
        Only checks if function values are equal in range of +100 to -100 of each variable
    """
    if expected.vars != got.vars:
        print("Variable set for expected is: %s\n but the got variable set is: %s")
    variables = [str(x) for x in expected.vars]

    equal = True
    for i in range(1000):
        # generate random input for the polynomials
        valueList = [random() * 200 - 100 for var in variables]
        varDict = {}
        for var, value in zip(variables, valueList):
            varDict[var] = value

        # check if the values of the polynomials are close enough
        if abs(expected.eval(varDict) - got.eval(varDict)) > 0.000001:
            equal = False
    if not equal:
        print("The given polynomials are not equal")


def randPoly(variables, depth, symbol):
    if depth == 1:
        poly = Polynomial()
        if symbol == "*":
            poly.poly = ["*"]
        else:
            poly.poly = ["+"]

        varsUsed = set()
        for i in range(2):
            if random() < 0.5:
                poly.poly.append(100 * random() - 50)
            else:
                var = choice(variables)
                varsUsed.add(var)
                poly.poly.append(var)

        poly.vars = varsUsed
        return poly
    else:
        poly = Polynomial()
        poly.poly = [symbol]
        varsUsed = set()
        for i in range(randint(2, 5)):
            if symbol == "*":
                newPoly = randPoly(variables, depth - 1, "+")
            elif symbol == "+":
                newPoly = randPoly(variables, depth - 1, "*")

            poly.poly.append(newPoly)
            varsUsed = varsUsed | newPoly.vars

        poly.vars = varsUsed
        return poly


x = Variable("x")
y = Variable("y")

((x + 2) * (y + 5)).simplify()

# for i in range(20):
#     print(i)
#     po = randPoly([x, y], 2, "*")
#     simplified = po.simplify()
#     comparePoly(po, simplified)
#
# for i in range(20):
#     print(i)
#     po = randPoly([x, y], 3, "*")
#     simplified = po.simplify()
#     comparePoly(po, simplified)

