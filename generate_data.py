import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate 30 days of hourly data
start_date = datetime(2024, 11, 1)
end_date = datetime(2024, 11, 30, 23, 59)
dates = pd.date_range(start=start_date, end=end_date, freq='H')
n_samples = len(dates)

print(f"Generating {n_samples} samples...")

# Base values  with realistic variation
data = {
    'timestamp': dates,
    'temperature': np.random.normal(25, 1.5, n_samples),
    'humidity': np.random.normal(55, 8, n_samples),
    'co2': np.random.normal(700, 150, n_samples),
    'noise': np.random.normal(50, 10, n_samples),
    'light': np.random.normal(350, 80, n_samples),
    'occupancy': np.random.randint(0, 5, n_samples)
}

df = pd.DataFrame(data)

# Add realistic pattern
df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek
df['is_weekend'] = df['day_of_week'] >= 5

# Class hour: Mon-Fri 8AM-4PM
class_hours = (
    (~df['is_weekend'])&
    (df['hour'] >= 8) &
    (df['hour'] <= 16)
)

# During class: higher temp, CO2, noise, occupancy
df.loc[class_hours, 'temperature'] += np.random.uniform(2, 4, class_hours.sum())
df.loc[class_hours, 'co2'] += np.random.uniform(300, 600, class_hours.sum())
df.loc[class_hours, 'noise'] += np.random.uniform(10, 25, class_hours.sum())
df.loc[class_hours, 'occupancy'] += np.random.randint(25, 40, class_hours.sum())
df.loc[class_hours, 'light'] += np.random.uniform(100, 200, class_hours.sum())

# Weekend/night: lower values
df.loc[~class_hours, 'occupancy'] = 0
df.loc[~class_hours, 'light'] = np.random.uniform(10, 100, (~class_hours).sum())

# Ensure realistic  bounds
df['temperature'] = df['temperature'].clip(20, 32)
df['humidity'] = df['humidity'].clip(30, 80)
df['co2'] = df['co2'].clip(400, 2000)
df['noise'] = df['noise'].clip(30, 85)
df['light'] = df['light'].clip(0,800)
df['occupancy'] = df['occupancy'].clip(0, 40)

# Save to CSV
df.to_csv('classroom_data.csv', index=False)
print(f"Data saved to classroom_data.csv")
print(f"Shape: {df.shape}")
print(f"\nFirst 5 rows: ")
print(df.head())