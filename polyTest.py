from Polynomial import Polynomial
from Variable import Variable

p = Polynomial(22)
p = p + 2
print(p)

p = p * p
print(p)

x = Variable("x")

p = x + p * x
print(p)

y = Variable("y")
q = Polynomial(3)
q = y + q

for x in p.vars:
    print(x)
print()

for x in q.vars:
    print(x)
print()

for x in (p + q).vars:
    print(x)

x = Variable("x")
y = Variable("y")
print(x + y)
print("x+y")

p1 = ((2 * y) + x)
p2 = ((x + y) * 10)
p3 = (y * x) ** 10
print(p1)
print(p2)
p = p1 * p2 + p3
print(p)
print("p")

p = 2 + x + 4 + y
q = 2 + x + (4 * y)
r = (2 + x) * (4 * y)
print(p, q, r)
print(p + q)

print(q)
print(q.eval({"x": 10, "y": 0}))
print(q.eval({"x": 10, "y": -3}))

print()
po = (2 + x) * (4 + x)
print(po)
print(po.simplify())
