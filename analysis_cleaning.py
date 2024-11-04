import os
import json
import heapq
import logging
from time import time
from collections import defaultdict
from statistics import mean
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def process_flight_data(folder_path: str):
    """Process flight data from JSON files in a specified folder.

    Args:
        folder_path (str): Path to the folder containing flight data JSON files.

    Returns:
        dict: Processed statistics including total records, dirty records, run duration, top cities, 
              and city passenger counts.
    """
    start_time = time()
    
    # Initialize counters and statistics
    total_records = 0
    dirty_records = 0
    city_stats = defaultdict(lambda: {'count': 0, 'total_duration': 0, 'durations': []})
    flight_durations = {}
    passenger_count = defaultdict(int)
    
    # Process each file in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if not os.path.isfile(file_path):
            logging.warning(f"Skipping non-file {file_path}")
            continue
        
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                for record in data:
                    total_records += 1
                    
                    # Check for dirty records
                    if any(value in [None, 0] for value in record.values()):
                        dirty_records += 1
                        continue
                    
                    # Extract record details
                    destination_city = record.get('destination_city')
                    origin_city = record.get('origin_city')
                    duration = record.get('flight_duration_secs', 0)
                    passengers = record.get('passengers_on_board', 0)
                    
                    # Update flight durations and passenger counts
                    if destination_city:
                        flight_durations.setdefault(destination_city, []).append(duration)
                        passenger_count[origin_city] -= passengers
                        passenger_count[destination_city] += passengers
                        
                        # Update city statistics
                        city_stats[destination_city]['count'] += 1
                        city_stats[destination_city]['durations'].append(duration)
                        city_stats[destination_city]['total_duration'] += duration

        except json.JSONDecodeError as e:
            logging.error(f"Error processing file {file_name}: {e}")
    
    # Generate summary statistics
    run_duration = time() - start_time
    top_25_cities = heapq.nlargest(25, city_stats.items(), key=lambda item: item[1]['count'])
    max_arrived_city = max(passenger_count, key=passenger_count.get, default=None)
    max_departed_city = min(passenger_count, key=passenger_count.get, default=None)
    
    # Output statistics
    logging.info(f"Total records processed: {total_records}")
    logging.info(f"Dirty records: {dirty_records}")
    logging.info(f"Total run duration: {run_duration:.2f} seconds")
    
    # Log top 25 cities
    top_cities_data = []
    for city, stats in top_25_cities:
        avg_duration = stats['total_duration'] / stats['count'] if stats['count'] > 0 else 0
        p95_duration = np.percentile(stats['durations'], 95) if stats['durations'] else None
        top_cities_data.append({
            'city': city,
            'average_duration': avg_duration,
            'p95_duration': p95_duration
        })
        logging.info(f"City: {city}, Average Duration: {avg_duration:.2f} seconds, P95 Duration: {p95_duration:.2f}")
    
    logging.info(f"City with max passengers arrived: {max_arrived_city}")
    logging.info(f"City with max passengers departed: {max_departed_city}")
    
    # Return structured results for testing or further processing
    return {
        'total_records': total_records,
        'dirty_records': dirty_records,
        'run_duration': run_duration,
        'top_cities': top_cities_data,
        'max_arrived_city': max_arrived_city,
        'max_departed_city': max_departed_city
    }

if __name__ == "__main__":
    # Use an environment variable or configuration for folder_path in production
    folder_path = "/tmp/flights"
    process_flight_data(folder_path)
