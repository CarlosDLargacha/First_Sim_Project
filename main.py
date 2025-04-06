import argparse
import numpy as np
from simulation.system1 import simulate_system1
from simulation.system2 import simulate_system2
from analyzer import analyze_results, print_system_results, compare_systems, generate_comparison_plots
from utils.logger import get_logger
from utils.config import *

# Configuración del logger
logger = get_logger(__name__)

def run_simulation(system_type, simulation_time, num_replications=5):
    """
    Ejecuta múltiples réplicas de la simulación y calcula promedios
    """
    all_results = []
    
    for rep in range(num_replications):
        logger.info(f"\nRéplica {rep + 1}/{num_replications}")
        
        if system_type == 1:
            results = simulate_system1(simulation_time)
        elif system_type == 2:
            results = simulate_system2(simulation_time)
        else:
            raise ValueError("Tipo de sistema no válido. Use 1 (M/M/2) o 2 (M/M/1)")
        
        all_results.append(results)
    
    # Calcular promedios entre réplicas
    avg_results = {
        'avg_wait_time': np.mean([r['avg_wait_time'] for r in all_results]),
        'avg_service_time': np.mean([r['avg_service_time'] for r in all_results]),
        'avg_queue_length': np.mean([r['avg_queue_length'] for r in all_results]),
        'utilization': np.mean([r['utilization'] for r in all_results]),
        'trucks_processed': int(np.mean([r['trucks_processed'] for r in all_results])),
        'raw_data': {
            'wait_times': np.concatenate([r['raw_data']['wait_times'] for r in all_results]),
            'service_times': np.concatenate([r['raw_data']['service_times'] for r in all_results]),
            'queue_lengths': np.concatenate([r['raw_data']['queue_lengths'] for r in all_results]),
            'utilization': np.concatenate([r['raw_data']['utilization'] for r in all_results])
        }
    }
    
    return avg_results

def main():
    parser = argparse.ArgumentParser(description='Simulación de sistemas de mantenimiento para camiones')
    parser.add_argument('--sistema', type=int, choices=[1, 2, 3], default=3,
                      help='1: Sistema M/M/2, 2: Sistema M/M/1, 3: Ambos (default)')
    parser.add_argument('--duracion', type=float, default=10080,
                      help='Duración de la simulación en minutos (default: 10080 = 1 semana)')
    parser.add_argument('--replicas', type=int, default=5,
                      help='Número de réplicas de la simulación (default: 5)')
    parser.add_argument('--graficos', action='store_true',
                      help='Generar gráficos comparativos')
    
    args = parser.parse_args()

    try:
        if args.sistema in [1, 2]:
            # Simular un solo sistema
            logger.info(f"\nIniciando simulación del Sistema {args.sistema}")
            results = run_simulation(args.sistema, args.duracion, args.replicas)
            print_system_results(results)
            
            if args.graficos:
                # Generar gráficos individuales
                generate_comparison_plots(results, None)
                
        else:
            # Simular ambos sistemas y comparar
            logger.info("\nIniciando simulación comparativa de ambos sistemas")
            
            logger.info("\nSimulando Sistema 1 (M/M/2)")
            results_sys1 = run_simulation(1, args.duracion, args.replicas)
            
            logger.info("\nSimulando Sistema 2 (M/M/1)")
            results_sys2 = run_simulation(2, args.duracion, args.replicas)
            
            # Comparación completa
            compare_systems({
                'sistema1': results_sys1,
                'sistema2': results_sys2
            })
            
            if args.graficos:
                generate_comparison_plots(results_sys1, results_sys2)
                
    except Exception as e:
        logger.error(f"Error durante la simulación: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()