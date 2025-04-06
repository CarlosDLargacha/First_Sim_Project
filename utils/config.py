# Parámetros de la simulación
SIMULATION_TIME = 10080  # 1 semana en minutos (60*24*7)
ARRIVAL_RATE = 1/40     # 1 camión cada 40 minutos
SERVICE_RATE_SYSTEM1 = 1/30  # 30 minutos por camión (2 servidores)
SERVICE_RATE_SYSTEM2 = 1/15  # 15 minutos por camión (1 servidor)

# Parámetros económicos
COST_WAITING = 2.0     # € por minuto de espera
COST_SYSTEM1 = 1.0     # € por minuto por servidor (2 servidores)
MAX_COST_SYSTEM2 = 2.55 # € máximo para que sea rentable