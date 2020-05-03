from Polynomial import Polynomial
from Variable import Variable
from random import random


def compare(expected, got):
    """ Compare two strings
    """
    if expected != got:
        print("Test case failed.\nExpected: %s\nBut got: %s" % (expected, got))


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
        valueList = [random() * 200 - 100 for var in variables]
        varDict = {}
        for var, value in zip(variables, valueList):
            varDict[var] = value
        if expected.eval(varDict) != got.eval(varDict):
            equal = False
    if not equal:
        print("The given polynomials are not equal")


# make sure that the basic polynomial contructor is working
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


x = Variable("x")
y = Variable("y")
compare("(x+y)", str(x + y))

p1 = ((2 * y) + x)
p2 = ((x + y) * 10)
p3 = (y * x) ** 10
p = p1 * p2 + p3
expectedString = "(((x+y)*10*((y*2)+x))+((y*x)^10))"
compare(expectedString, str(p))


p = 2 + x + 4 + y
q = 2 + x + (4 * y)
r = (2 + x) * (4 * y)
compare("(x+2+4+y)", str(p))
compare("(x+2+(y*4))", str(q))
compare("(y*4*(x+2))", str(r))

q1 = q.eval({"x": 10, "y": 0})
compare(q1, 2)
q2 = q.eval({"x": 10, "y": -3})
compare(q1, 1)

print()
po = (2 + x) * (4 + x)
simplified = po.simplify()
comparePoly(po, simplified)
