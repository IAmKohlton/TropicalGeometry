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
