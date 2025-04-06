import simpy
import numpy as np
from utils.config import *
from utils.logger import get_logger

logger = get_logger(__name__)

class Truck:
    def __init__(self, truck_id, arrival_time):
        self.id = truck_id
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.departure_time = None

def simulate_system2(simulation_time):
    """Simula el sistema M/M/1 con servidor rápido"""
    env = simpy.Environment()
    service_station = simpy.Resource(env, capacity=1)
    results = {
        'wait_times': [],
        'service_times': [],
        'queue_lengths': [],
        'trucks_processed': 0,
        'utilization': []
    }

    def truck_process(env, truck, service_station, results):
        logger.debug(f"Camion {truck.id} llega al sistema a tiempo {truck.arrival_time:.2f}")

        with service_station.request() as request:
            yield request
            truck.service_start_time = env.now
            wait_time = truck.service_start_time - truck.arrival_time
            results['wait_times'].append(wait_time)

            service_time = np.random.exponential(1/SERVICE_RATE_SYSTEM2)
            results['service_times'].append(service_time)
            yield env.timeout(service_time)

            truck.departure_time = env.now
            logger.debug(f"Camion {truck.id} sale a tiempo {truck.departure_time:.2f}")
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
            busy_servers = service_station.count
            utilization = busy_servers / service_station.capacity
            results['utilization'].append(utilization)
            yield env.timeout(1.0)

    env.process(truck_generator(env, service_station, results))
    env.process(monitor(env, service_station, results))
    env.run(until=simulation_time)

    metrics = calculate_metrics(results)
    logger.info(f"Simulación Sistema 2 completada. Camiones procesados: {metrics['trucks_processed']}")
    return metrics

def calculate_metrics(results):
    return {
        'avg_wait_time': np.mean(results['wait_times']) if results['wait_times'] else 0,
        'avg_service_time': np.mean(results['service_times']) if results['service_times'] else 0,
        'avg_queue_length': np.mean(results['queue_lengths']) if results['queue_lengths'] else 0,
        'utilization': np.mean(results['utilization']) if results['utilization'] else 0,
        'trucks_processed': results['trucks_processed'],
        'raw_data': results
    }