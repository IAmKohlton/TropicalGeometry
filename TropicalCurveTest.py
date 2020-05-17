import unittest
from Variable import Variable
from TropicalCurve import TropicalCurve
from Polynomial import Polynomial
from testUtilities import assertThrows, assertDoesntThrow


class ConstructorTest(unittest.TestCase):

    def testInvalidConstructorInteger(self):
        assertThrows(lambda: TropicalCurve(2), TypeError)

    def testInvalidConstructorVariable(self):
        x = Variable("x")
        assertThrows(lambda: TropicalCurve(x), TypeError)

    def testNotEnoughVariables(self):
        x = Variable("x")
        assertThrows(lambda: TropicalCurve(Polynomial(input=x)), ValueError)

    def testTooManyVariables(self):
        x = Variable("x")
        y = Variable("y")
        z = Variable("z")
        assertThrows(lambda: TropicalCurve(x + y + z), ValueError)

    def testProperConstructor(self):
        x = Variable("x")
        y = Variable("y")
        assertDoesntThrow(lambda: TropicalCurve(x + y))


if __name__ == "__main__":
    unittest.main()
