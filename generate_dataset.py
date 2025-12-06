import pandas as pd
import random
from datetime import datetime, timedelta
from bridge_sim import generate_bridge_data

# Configurations
RECORDS = 1000 # Number of data points
START_TIME = datetime.now() - timedelta(hours=24)

print(f"Generating {RECORDS} rows of structural health data...")

data_list = []
current_time = START_TIME

for i in range(RECORDS):
    # Simulate a mix of Normal (95%) and Critical (5%) data
    is_critical = random.random() > 0.95
    scenario = "critical" if is_critical else "normal"
    
    # Generate single data point
    row = generate_bridge_data(scenario)
    
    # Override timestamp to make it a time-series
    row['timestamp'] = current_time.isoformat()
    
    data_list.append(row)
    
    # Advance time by ~1.5 minutes
    current_time += timedelta(minutes=1.5)

# Create DataFrame
df = pd.DataFrame(data_list)

# Save to CSV
output_file = "bridge_data.csv"
df.to_csv(output_file, index=False)

print(f"✅ Success! Generated '{output_file}' with shape {df.shape}")
print("You can verify this file in Excel or use it for offline AI training.")
