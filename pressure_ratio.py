def calc_pressure_ratio(Me, gamma=1.4):
    return (1 + ((gamma - 1)/2) * Me**2) ** (-gamma / (gamma - 1))
