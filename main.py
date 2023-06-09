from expr import *

native_lambda = lambda x: x * (x - 1)
magic_lambda = X * (X - 1)

print(native_lambda(7))
# 42
print(magic_lambda(7))
# 42
print(magic_lambda(7, evaluator=Differentiator()))
# d(x * (x - 1))/dx = d(x**2 - x)/dx = 2*x - 1
# 13
