import numpy as np
import matplotlib.pyplot as plt
from utils.config import *
from utils.logger import get_logger

logger = get_logger(__name__)

def analyze_results(results):
    try:
        if isinstance(results, dict) and 'sistema1' in results and 'sistema2' in results:
            compare_systems(results)
        else:
            print_system_results(results)
    except Exception as e:
        logger.error(f"Error en el análisis: {str(e)}")
        raise

def print_system_results(results):
    """Muestra resultados de un solo sistema"""
    logger.info("\nRESULTADOS DE LA SIMULACIÓN")
    logger.info(f"• Tiempo promedio de espera: {results['avg_wait_time']:.2f} minutos")
    logger.info(f"• Tiempo promedio de servicio: {results['avg_service_time']:.2f} minutos")
    logger.info(f"• Longitud promedio de cola: {results['avg_queue_length']:.2f} camiones")
    logger.info(f"• Utilización del sistema: {results['utilization']:.2%}")
    logger.info(f"• Camiones procesados: {results['trucks_processed']}")

def compare_systems(results):
    """Compara los dos sistemas y genera gráficos"""
    sys1 = results['sistema1']
    sys2 = results['sistema2']
    
    # Análisis comparativo
    logger.info("\nCOMPARACIÓN ENTRE SISTEMAS")
    logger.info(f"• Diferencia en tiempo de espera: {sys1['avg_wait_time'] - sys2['avg_wait_time']:.2f} minutos")
    logger.info(f"• Mejora porcentual: {(sys1['avg_wait_time'] - sys2['avg_wait_time'])/sys1['avg_wait_time']:.2%}")
    
    # Análisis económico
    cost_sys1 = (sys1['avg_wait_time'] * COST_WAITING) + (2 * COST_SYSTEM1)
    cost_sys2 = (sys2['avg_wait_time'] * COST_WAITING) + MAX_COST_SYSTEM2
    
    logger.info("\nANÁLISIS ECONÓMICO")
    logger.info(f"• Costo total Sistema 1: {cost_sys1:.2f} €/min")
    logger.info(f"• Costo total Sistema 2: {cost_sys2:.2f} €/min")
    logger.info(f"• Diferencia de costos: {cost_sys1 - cost_sys2:.2f} €/min")
    
    # Generación de gráficos
    generate_comparison_plots(sys1, sys2)

def generate_comparison_plots(sys1, sys2):
    """Genera gráficos comparativos"""
    plt.figure(figsize=(15, 6))
    
    # Gráfico de tiempos de espera
    plt.subplot(1, 2, 1)
    plt.hist(sys1['raw_data']['wait_times'], bins=30, alpha=0.5, label='Sistema 1 (M/M/2)')
    plt.hist(sys2['raw_data']['wait_times'], bins=30, alpha=0.5, label='Sistema 2 (M/M/1)')
    plt.title('Distribución de Tiempos de Espera')
    plt.xlabel('Minutos')
    plt.ylabel('Frecuencia')
    plt.legend()
    
    # Gráfico de longitud de cola
    plt.subplot(1, 2, 2)
    plt.plot(sys1['raw_data']['queue_lengths'], label='Sistema 1 (M/M/2)', alpha=0.7)
    plt.plot(sys2['raw_data']['queue_lengths'], label='Sistema 2 (M/M/1)', alpha=0.7)
    plt.title('Evolución de la Longitud de Cola')
    plt.xlabel('Evento')
    plt.ylabel('Camiones en cola')
    plt.legend()
    
    plt.show()
    
    #plt.tight_layout()
    #plt.savefig('report/figures/comparison.png')
    #logger.info("Gráficos generados en report/figures/comparison.png")