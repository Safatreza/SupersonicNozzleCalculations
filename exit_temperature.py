def calc_static_exit_temperature(T0, Me, gamma=1.4):
    return T0 / (1 + ((gamma - 1) / 2) * Me**2)
