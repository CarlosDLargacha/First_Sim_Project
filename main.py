import argparse
import numpy as np
from simulation.system1 import simulate_system1
from simulation.system2 import simulate_system2
from analyzer import analyze_results
from utils.logger import get_logger
from utils.config import *

logger = get_logger(__name__)

# Hipótesis a validar
HIPOTESIS = {
    "H1": "El Sistema 2 reducirá el tiempo de espera en al menos 25%",
    "H2": "El costo adicional del Sistema 2 no excederá 3€/minuto",
    "H3": "Ambos sistemas alcanzarán estado estable antes de 5000 minutos"
}

def main():
    parser = argparse.ArgumentParser(description='Simulación de sistemas de mantenimiento')
    parser.add_argument('--sistema', type=int, choices=[1, 2, 3], default=3,
                      help='Sistema a simular: 1 (M/M/2), 2 (M/M/1), 3 (Ambos)')
    parser.add_argument('--duracion', type=float, default=SIMULATION_TIME,
                      help=f'Duración de la simulación en minutos (default: {SIMULATION_TIME})')
    parser.add_argument('--replicas', type=int, default=5,
                      help='Número de réplicas independientes (default: 5)')
    
    args = parser.parse_args()

    try:
        logger.info("\nConfiguración inicial:")
        logger.info(f"- Duración: {args.duracion} minutos")
        logger.info(f"- Réplicas: {args.replicas}")
        logger.info("\nHipótesis a validar:")
        for h in HIPOTESIS.values():
            logger.info(f"- {h}")

        if args.sistema in [1, 2]:
            results = run_simulation(args.sistema, args.duracion, args.replicas)
        else:
            logger.info("\nSimulando ambos sistemas...")
            results = {
                'sistema1': run_simulation(1, args.duracion, args.replicas),
                'sistema2': run_simulation(2, args.duracion, args.replicas)
            }
        
        analyze_results(results)
        logger.info("\nProceso completado exitosamente")

    except Exception as e:
        logger.error(f"\nError en la simulación: {str(e)}", exc_info=True)
        raise

def run_simulation(system_type, simulation_time, num_replications):
    """Ejecuta múltiples réplicas y consolida resultados"""
    all_results = []
    for rep in range(num_replications):
        logger.info(f"\nRéplica {rep+1}/{num_replications}")
        if system_type == 1:
            result = simulate_system1(simulation_time)
        else:
            result = simulate_system2(simulation_time)
        all_results.append(result)
    
    # Consolidar resultados
    return {
        'avg_wait_time': np.mean([r['avg_wait_time'] for r in all_results]),
        'avg_service_time': np.mean([r['avg_service_time'] for r in all_results]),
        'avg_queue_length': np.mean([r['avg_queue_length'] for r in all_results]),
        'trucks_processed': np.mean([r['trucks_processed'] for r in all_results]),
        'utilization': np.mean([r['utilization'] for r in all_results]),
        'raw_data': {
            'wait_times': np.concatenate([r['raw_data']['wait_times'] for r in all_results]),
            'queue_lengths': np.concatenate([r['raw_data']['queue_lengths'] for r in all_results]),
            'convergence': [r['raw_data']['queue_lengths'] for r in all_results]
        }
    }

if __name__ == "__main__":
    main()