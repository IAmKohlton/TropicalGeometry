import unittest
from testUtilities import assertThrows, assertDoesntThrow
from Ray import Ray
from math import pi, atan


class TestConstructor(unittest.TestCase):
    def testEmptyConstructor(self):
        assertThrows(lambda: Ray(), Exception)

    def testSingleVariableRayThrows(self):
        assertThrows(lambda: Ray({"x": 0}, 0, 1), ValueError)

    def testTooManyVariablesThrows(self):
        assertThrows(lambda: Ray({"x": 0, "y": 0, "z": 0}, 0, 1), ValueError)

    def testAngleGreaterThan2pi(self):
        assertThrows(lambda: Ray({"x": 0, "y": 0}, 2 * pi, 1), ValueError)

    def testAngleLessThan0(self):
        assertThrows(lambda: Ray({"x": 0, "y": 0}, -0.1, 1), ValueError)

    def testDistanceCantBeZero(self):
        assertThrows(lambda: Ray({"x": 0, "y": 0}, 1, 0), ValueError)

    def testDistanceCantBeLessThanZero(self):
        assertThrows(lambda: Ray({"x": 0, "y": 0}, 1, -1), ValueError)

    def testPointNotInXY(self):
        assertThrows(lambda: Ray({"x": 0, "z": 0}, 0, 1), ValueError)

    def testValidConstructor(self):
        assertDoesntThrow(lambda: Ray({"x": 0, "y": 0}, 1, 1))

    def testEqualRays(self):
        ray1 = Ray({"x": 0, "y": 0}, 0, 1)
        ray2 = Ray({"x": 0, "y": 0}, 0, 1)
        assert ray1 == ray2

    def testRaysNotEqualPoint(self):
        ray1 = Ray({"x": 0, "y": 0}, 0, 1)
        ray2 = Ray({"x": 1, "y": 0}, 0, 1)
        assert ray1 != ray2

    def testRaysNotEqualAngles(self):
        ray1 = Ray({"x": 0, "y": 0}, 0, 1)
        ray2 = Ray({"x": 0, "y": 0}, 1, 1)
        assert ray1 != ray2

    def testRaysNotEqualDistances(self):
        ray1 = Ray({"x": 0, "y": 0}, 0, 1)
        ray2 = Ray({"x": 0, "y": 0}, 0, 2)
        assert ray1 != ray2

    def testRaysOppositeEachother(self):
        ray1 = Ray({"x": 0, "y": 0}, 0, 1)
        ray2 = Ray({"x": 1, "y": 0}, pi, 1)
        assert ray1 == ray2

    def testGetEndPointHorizontalAngle(self):
        expectedPoint = {"x": 5, "y": 5}
        ray = Ray({"x": 0, "y": 5}, 0, 5)
        assert Ray.pointsVeryClose(ray.getEndPoint(), expectedPoint)

    def testGetEndPointVerticalAngle(self):
        expectedPoint = {"x": 5, "y": 5}
        ray = Ray({"x": 5, "y": 0}, pi / 2, 5)
        assert Ray.pointsVeryClose(ray.getEndPoint(), expectedPoint)

    def testGetEndPointBackwards(self):
        expectedPoint = {"x": 1, "y": 1}
        ray = Ray({"x": 5, "y": 4}, atan(3 / 4) + pi, 5)
        assert Ray.pointsVeryClose(ray.getEndPoint(), expectedPoint)

    def testGetEndPointOnAngle(self):
        expectedPoint = {"x": 1, "y": 1}
        ray = Ray({"x": 0, "y": 0}, pi / 4, 2**0.5)
        assert Ray.pointsVeryClose(ray.getEndPoint(), expectedPoint)


if __name__ == "__main__":
    unittest.main()
