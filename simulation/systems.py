import math

def sistema_MM2(lambda_, mu, s=2):
    """
    Calcula las métricas para un sistema M/M/s (en este caso, M/M/2).
    
    Parámetros:
        lambda_: Tasa de llegadas (camiones/minuto).
        mu: Tasa de servicio por servidor (camiones/minuto).
        s: Número de servidores (por defecto 2).
    
    Retorna:
        L: Número promedio de camiones en el sistema.
        W: Tiempo promedio en el sistema (minutos).
        P0: Probabilidad de que no haya camiones en el sistema.
    """
    rho = lambda_ / (s * mu)
    
    if rho >= 1:
        raise ValueError("El sistema no es estable (rho >= 1).")
    
    # Cálculo de P0
    sum_part = sum((s * rho)**n / math.factorial(n) for n in range(s))
    P0 = 1 / (sum_part + (s * rho)**s / (math.factorial(s) * (1 - rho)))
    
    # Cálculo de Lq (camiones en cola)
    Lq = (P0 * (s * rho)**s * rho) / (math.factorial(s) * (1 - rho)**2)
    
    # Cálculo de L (camiones en el sistema)
    L = Lq + lambda_ / mu
    
    # Cálculo de W (tiempo en el sistema)
    W = L / lambda_
    
    return L, W, P0

def sistema_MM1(lambda_, mu):
    """
    Calcula las métricas para un sistema M/M/1.
    
    Parámetros:
        lambda_: Tasa de llegadas (camiones/minuto).
        mu: Tasa de servicio (camiones/minuto).
    
    Retorna:
        L: Número promedio de camiones en el sistema.
        W: Tiempo promedio en el sistema (minutos).
    """
    rho = lambda_ / mu
    
    if rho >= 1:
        raise ValueError("El sistema no es estable (rho >= 1).")
    
    # Cálculo de L (camiones en el sistema)
    L = rho / (1 - rho)
    
    # Cálculo de W (tiempo en el sistema)
    W = L / lambda_
    
    return L, W

def comparar_costos(lambda_, mu1, mu2, cost_per_minute_camion=2, cost_system1_per_minute=1):
    """
    Compara los costos de los dos sistemas y calcula el costo máximo que puede tener
    el Sistema 2 para que no haya diferencia económica.
    """
    # Calculamos métricas para ambos sistemas
    L1, W1, _ = sistema_MM2(lambda_, mu1)
    L2, W2 = sistema_MM1(lambda_, mu2)
    
    # Costo total del Sistema 1
    total_cost1 = (L1 * cost_per_minute_camion) + cost_system1_per_minute
    
    # Costo máximo del Sistema 2 para igualar costos
    cost_system2_per_minute = total_cost1 - (L2 * cost_per_minute_camion)
    
    # Resultados
    print("=== Sistema 1 (M/M/2) ===")
    print(f"Número promedio de camiones en el sistema (L1): {L1:.4f}")
    print(f"Tiempo promedio en el sistema (W1): {W1:.2f} minutos")
    print(f"Costo total por minuto: {total_cost1:.2f} euros")
    
    print("\n=== Sistema 2 (M/M/1) ===")
    print(f"Número promedio de camiones en el sistema (L2): {L2:.4f}")
    print(f"Tiempo promedio en el sistema (W2): {W2:.2f} minutos")
    print(f"Costo máximo para igualar al Sistema 1: {cost_system2_per_minute:.2f} euros/minuto")
    
    return cost_system2_per_minute

