import json
import random
import datetime
from pathlib import Path
from statistics import mean, quantiles
from collections import Counter, defaultdict

total_files = 5000
cities  = random.randint(100, 200)

cities = [f"City_{i}" for i in range(cities)]

def get_date():
    start = datetime.datetime(2024, 1, 1)
    end = datetime.datetime(2025, 1, 1)
    return (start + datetime.timedelta(seconds=random.randint(0, int((end - start).total_seconds())))).isoformat()

output_dir = Path("/tmp/flights")
output_dir.mkdir(parents=True, exist_ok=True)


m_min, n_max = 50, 100

for i in range(total_files):
    origin_city = random.choice(cities)
    month_year = datetime.datetime.now().strftime("%m-%y")
    file_path = output_dir / f"{month_year}-{origin_city}-flights.json"
    records = []
    
    for i in range(random.randint(m_min, n_max)):
        record = {
            "date": get_date() ,
            "origin_city": origin_city  ,
            "destination_city": random.choice(cities) ,
            "flight_duration_secs": random.randint(1800, 10800) ,
            "passengers_on_board": random.randint(1, 300) 
        }
        records.append(record)

    with open(file_path, "w") as f:
        json.dump(records, f)
