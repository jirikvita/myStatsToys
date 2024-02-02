#!/usr/bin/python

power_generator = lambda n: (lambda x: x ** n)

# Example usage
doubler = power_generator(2)
tripler = power_generator(3)
quadrupler = power_generator(4)

# Use the generated functions
value = 5

doubled_value = doubler(value)
tripled_value = tripler(value)
quadrupled_value = quadrupler(value)

print(f"Original value: {value}")
print(f"Doubled value: {doubled_value}")
print(f"Tripled value: {tripled_value}")
print(f"Quadrupled value: {quadrupled_value}")
