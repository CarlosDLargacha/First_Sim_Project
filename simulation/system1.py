import simpy
import numpy as np
from utils.logger import get_logger
from utils.config import *

logger = get_logger(__name__)

class Truck:
    def __init__(self, truck_id, arrival_time):
        self.id = truck_id
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.departure_time = None

def simulate_system1(simulation_time):  
    """Versión corregida con almacenamiento garantizado de service_times"""
    env = simpy.Environment()
    service_station = simpy.Resource(env, capacity=2) 
    results = {
        'wait_times': [],
        'service_times': [], 
        'queue_lengths': [],
        'trucks_processed': 0,
        'utilization': []
    }

    def truck_process(env, truck, service_station, results):
        with service_station.request() as request:
            yield request
            truck.service_start_time = env.now
            results['wait_times'].append(truck.service_start_time - truck.arrival_time)
            
            # Parte CRUCIAL: Generar y guardar el tiempo de servicio
            service_time = np.random.exponential(1/SERVICE_RATE_SYSTEM1)  # SERVICE_RATE_SYSTEM2 para system2
            results['service_times'].append(service_time)  # Almacenamiento garantizado
            yield env.timeout(service_time)
            
            truck.departure_time = env.now
            results['trucks_processed'] += 1

    def truck_generator(env, service_station, results):
        truck_count = 0
        while True:
            yield env.timeout(np.random.exponential(1/ARRIVAL_RATE))
            truck_count += 1
            truck = Truck(truck_count, env.now)
            env.process(truck_process(env, truck, service_station, results))
            results['queue_lengths'].append(len(service_station.queue))

    def monitor(env, service_station, results):
        while True:
            results['utilization'].append(service_station.count / service_station.capacity)
            yield env.timeout(1.0)

    env.process(truck_generator(env, service_station, results))
    env.process(monitor(env, service_station, results))
    env.run(until=simulation_time)

    # Métricas finales con estructura de datos consistente
    return {
        'avg_wait_time': np.mean(results['wait_times']) if results['wait_times'] else 0,
        'avg_service_time': np.mean(results['service_times']) if results['service_times'] else 0,
        'avg_queue_length': np.mean(results['queue_lengths']) if results['queue_lengths'] else 0,
        'utilization': np.mean(results['utilization']) if results['utilization'] else 0,
        'trucks_processed': results['trucks_processed'],
        'raw_data': {
            'wait_times': np.array(results['wait_times']),
            'service_times': np.array(results['service_times']), 
            'queue_lengths': np.array(results['queue_lengths']),
            'utilization': np.array(results['utilization'])
        }
    }