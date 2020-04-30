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
