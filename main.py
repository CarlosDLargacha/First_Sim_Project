from simulation.systems import *

# Parámetros del problema
lambda_ = 1 / 40  # tasa de llegadas (camiones/minuto)
mu1 = 1 / 30      # tasa de servicio por servidor en Sistema 1
mu2 = 1 / 15      # tasa de servicio en Sistema 2

# Comparar los sistemas
cost_system2 = comparar_costos(lambda_, mu1, mu2)