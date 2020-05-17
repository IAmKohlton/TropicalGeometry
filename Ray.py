from math import pi, sin, cos


class Ray(object):
    def __init__(self, point, angle, distance):
        # this class makes the assumption that the x axis has angle=0
        if set(point.keys()) != {"x", "y"}:
            raise ValueError("point must be a dict with keys x, y")
        if angle >= 2 * pi or angle < 0:
            raise ValueError("angle can't be larger than 2pi or smaller than 0")
        if distance <= 0:
            raise ValueError("distance can't be equal to or less than 0")
        self.point = point
        self.angle = angle
        self.distance = distance

    def __eq__(self, other):
        if other.distance == self.distance == float("inf"):
            return self.bothDistancesInfinity(other)
        pointsEqual = Ray.pointsVeryClose(self.point, other.point)
        anglesEqual = Ray.floatEqual(self.angle, other.angle)
        distanceEqual = Ray.floatEqual(self.distance, other.distance)

        if distanceEqual and self.anglesAreOppositeEachother(other):
            return Ray.pointsVeryClose(self.point, other.getEndPoint())
        else:
            return pointsEqual and anglesEqual and distanceEqual

    def anglesAreOppositeEachother(self, other):
        return Ray.floatEqual(self.angle % (2 * pi), (other.angle + pi) % (2 * pi))

    def getEndPoint(self):
        x = self.point["x"] + self.distance * cos(self.angle)
        y = self.point["y"] + self.distance * sin(self.angle)
        return {"x": x, "y": y}

    @staticmethod
    def pointsVeryClose(selfPoint, otherPoint):
        xVeryClose = Ray.floatEqual(selfPoint["x"], otherPoint["x"])
        yVeryClose = Ray.floatEqual(selfPoint["y"], otherPoint["y"])
        return xVeryClose and yVeryClose

    @staticmethod
    def floatEqual(float1, float2):
        return abs(float1 - float2) < 0.000001

    def bothDistancesInfinity(self, other):
        pass
