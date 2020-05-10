from Polynomial import Polynomial
from Variable import Variable
from random import random
from random import randint
from random import choice
from inspect import stack


def seeWhereErrorHappened():
    stackinfo = stack()
    return stackinfo[-1].lineno


def compare(expected, got):
    """ Compare two strings
    """
    if expected != got:
        print("Test case failed on line %i.\nExpected: %s\nBut got: %s" % (seeWhereErrorHappened(), expected, got))


def compareSet(expected, got):
    """ Compare two sets by casting elements to strings
        Made for the q.vars parameter especially
    """
    newExpected = set()
    for el in expected:
        newExpected.add(str(el))
    newGot = set()
    for el in got:
        newGot.add(str(el))
    compare(newExpected, newGot)


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
        print("The polynomials on line %i are not equal" % seeWhereErrorHappened())


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


p = Polynomial(22)
p = p + 2
expectedString = "(22+2)"
compare(expectedString, str(p))


p = p * p
expectedString = "((22+2)*(22+2))"
compare(expectedString, str(p))


x = Variable("x")
p = x + p * x
expectedString = "(x+((22+2)*(22+2)*x))"
compare(expectedString, str(p))


y = Variable("y")
q = Polynomial(3)
q = y + q
expectedString = "(y+q)"


expectedSet = {"x"}
compareSet(expectedSet, p.vars)


expectedSet = {"y"}
compareSet(expectedSet, q.vars)


expectedSet = {"x", "y"}
compareSet(expectedSet, (p + q).vars)

singleVarPoly = x + 1
singleVarPoly = Polynomial(input=singleVarPoly)
expectedSet = {"x"}
compareSet(expectedSet, singleVarPoly.vars)


x = Variable("x")
y = Variable("y")
compare("(x+y)", str(x + y))


p1 = ((2 * y) + x)
p2 = ((x + y) * 10)
p3 = (y * x) ** 10
p = p1 * p2 + p3
expectedString = "((((y*2)+x)*(x+y)*10)+((y*x)^10))"
compare(expectedString, str(p))


p = 2 + x + 4 + y
q = 2 + x + (4 * y)
r = (2 + x) * (4 * y)
compare("(x+2+4+y)", str(p))
compare("(x+2+(y*4))", str(q))
compare("((x+2)*y*4)", str(r))


q1 = q.eval({"x": 10, "y": 0})
compare(q1, 2)
q2 = q.eval({"x": 10, "y": -3})
compare(q2, 1)


po = (2 + x) * (4 + x)
simplified = po.simplify()
comparePoly(po, simplified)


po = ((x * 2) + (y * (-4))) * (x + (x * y)) * ((20 * y) + (x * x) + (y * x * y))
simplified = po.simplify()
comparePoly(po, simplified)


po = (((1 + x) * (2 + y)) + ((x + y) * (x + (-5)))) * (((y + y) * (x + x)) + ((4 + x) * (x + 10)))
simplified = po.simplify()
comparePoly(po, simplified)


po = (1 + x) ** 2
expectedPoly = 2 + 1 * x + x ** 2
comparePoly(po.simplify(), simplified)


x = Variable("x")
y = Variable("y")
for i in range(10):
    po = randPoly([x, y], 2, "*")
    simplified = po.simplify()
    comparePoly(po, simplified)

for i in range(5):
    po = randPoly([x, y], 3, "*")  # never change this number to be larger than 3
    simplified = po.simplify()
    comparePoly(po, simplified)
