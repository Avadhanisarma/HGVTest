import os
import json
import heapq
import numpy as np

from time import time
from collections import Counter, defaultdict
from statistics import quantiles,mean



start_time = time()

folder_path = "/tmp/flights"

total_records = 0
dirty_records = 0

city_stats = defaultdict(lambda: {'count': 0, 'total_duration': 0,'durations':[]})



flight_durations = {}
passenger_count = {}

for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    
    if not os.path.isfile(file_path):
        continue
    with open(file_name, 'r') as file:
        try:
            data = json.load(file)
            for record in data:
                total_records += 1
                
                if any(value in [None,0] for value in record.values()):
                    dirty_records += 1
                    continue
    
                if record['destination_city']:
                    destination_city = record['destination_city']
                    duration = record['flight_duration_secs']
                    origin_city = record['origin_city']

                    if destination_city not in flight_durations:
                        flight_durations[destination_city] = []
                    flight_durations[destination_city].append(duration)

                    if origin_city not in passenger_count:
                        passenger_count[origin_city] = 0
                    if destination_city not in passenger_count:
                        passenger_count[destination_city]=0

                    passenger_count[origin_city]-=record['passengers_on_board']
                    passenger_count[destination_city] += record['passengers_on_board']

                       
                    city_stats[destination_city]['count'] += 1
                    city_stats[destination_city]['durations'].append(duration)
                    city_stats[destination_city]['total_duration'] += duration

                   
                   
        except json.JSONDecodeError as e:
            print(f"Error processing file {file_name}: {e}")



top_25_cities = heapq.nlargest(25, city_stats.items(), key=lambda item: item[1]['count'])


max_arrived_city = max(passenger_count, key=passenger_count.get)
max_departed_city = min(passenger_count, key=passenger_count.get)

end_time = time()
run_duration = end_time - start_time

print(f"Total records processed: {total_records}")
print(f"Dirty records: {dirty_records}")
print(f"Total run duration: {run_duration:.2f} seconds")
print("Top 25 destination cities:")
for city, stats in top_25_cities:
    avg_duration = stats['total_duration'] / stats['count'] if stats['count'] > 0 else 0
    p95_duration = np.percentile(stats['durations'], 95) if stats['durations'] else None
    print(f"City: {city}, , Average Duration: {avg_duration:.2f} seconds, P95 duration: {p95_duration:.2f}")

print(f"City with max passengers arrived: {max_arrived_city}")
print(f"City with max passengers departed: {max_departed_city}")
