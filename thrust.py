def calc_thrust(m_dot, Ve, Pe, Patm, Ae):
    return m_dot * Ve + (Pe - Patm) * Ae
