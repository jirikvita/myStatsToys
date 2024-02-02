#!/usr/bin/python

def power_generator(n):
    return lambda x, count: [ (x + i) ** n for i in range(count)]

# Example usage
doubler = power_generator(2)
tripler = power_generator(3)
quadrupler = power_generator(4)

# Use the generated functions
value = 2  # Starting value
count = 5  # Number of values to print

doubled_values = doubler(value, count)
tripled_values = tripler(value, count)
quadrupled_values = quadrupler(value, count)

print(f"start with {value} to the power of 2 for {count} values: {doubled_values}")
print(f"start with {value} to the power of 3 for {count} values: {tripled_values}")
print(f"start with {value} to the power of 4 for {count} values: {quadrupled_values}")
