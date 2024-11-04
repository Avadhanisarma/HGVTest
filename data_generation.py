import json
import random
import datetime
import logging
from pathlib import Path
from typing import List, Dict

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuration variables
TOTAL_FILES = 5000
NUM_CITIES = random.randint(100, 200)
OUTPUT_DIR = Path("/tmp/flights")
MIN_RECORDS_PER_FILE = 50
MAX_RECORDS_PER_FILE = 100

# Generate random city names
cities = [f"City_{i}" for i in range(NUM_CITIES)]

def get_random_date() -> str:
    """Generate a random ISO date between the start and end of 2024."""
    start = datetime.datetime(2024, 1, 1)
    end = datetime.datetime(2025, 1, 1)
    random_date = start + datetime.timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
    return random_date.isoformat()

def generate_flight_record(origin_city: str) -> Dict:
    """Generate a random flight record."""
    return {
        "date": get_random_date(),
        "origin_city": origin_city,
        "destination_city": random.choice(cities),
        "flight_duration_secs": random.randint(1800, 10800),
        "passengers_on_board": random.randint(1, 300)
    }

def create_flight_records_for_city(origin_city: str, num_records: int) -> List[Dict]:
    """Create multiple flight records for a given origin city."""
    return [generate_flight_record(origin_city) for _ in range(num_records)]

def save_records_to_file(records: List[Dict], file_path: Path):
    """Save flight records to a JSON file."""
    try:
        with open(file_path, "w") as file:
            json.dump(records, file)
        logging.info(f"Saved {len(records)} records to {file_path}")
    except IOError as e:
        logging.error(f"Failed to write to file {file_path}: {e}")

def main():
    """Main function to generate and save flight records for multiple files."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for i in range(TOTAL_FILES):
        origin_city = random.choice(cities)
        month_year = datetime.datetime.now().strftime("%m-%y")
        file_path = OUTPUT_DIR / f"{month_year}-{origin_city}-flights.json"
        num_records = random.randint(MIN_RECORDS_PER_FILE, MAX_RECORDS_PER_FILE)
        
        # Generate and save records
        records = create_flight_records_for_city(origin_city, num_records)
        save_records_to_file(records, file_path)

if __name__ == "__main__":
    main()
