"""

rho0 = 0.001225 # kg/m3, sea level
# https://link.springer.com/article/10.1007/s40828-020-0111-6
p0 = 1013e2 # Pa
g = 9.81    # ms-2
H = p0 / (rho0 * g)
def getPressure(h):
    p = p0 * exp(-h/H)
    return p
    
R = # constant
T = # temperature
M = # air molar mass
def getRho(h):
    rho = getPressure(h) * M  / (R*T)
    return rhi
"""
