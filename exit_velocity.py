import math

def calc_exit_velocity(cp, T0, Te):
    return math.sqrt(2 * cp * (T0 - Te))
