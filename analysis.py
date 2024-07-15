import csv
import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns

def parse_timestamps(in_timestamp_str, out_timestamp_str):
  try:
    in_timestamp = datetime.datetime.strptime(in_timestamp_str, "%Y-%m-%d %H:%M:%S")
    out_timestamp = datetime.datetime.strptime(out_timestamp_str, "%Y-%m-%d %H:%M:%S")
    if in_timestamp > out_timestamp:  # Check for invalid timestamps (in after out)
      print(f"Warning: Invalid timestamps for entry - in: {in_timestamp_str}, out: {out_timestamp_str}")
      return None
    duration = (out_timestamp - in_timestamp).total_seconds() / 3600  # Calculate duration in hours
    return duration
  except ValueError:  # Handle potential parsing errors
    print(f"Error parsing timestamps: in: {in_timestamp_str}, out: {out_timestamp_str}")
    return None

# Reads the data from parking_entries_exits.csv
data = []

with open("parking_entries_exits.csv", 'r') as csvfile:
  reader = csv.reader(csvfile)
  next(reader)
  for row in reader:
    numberplate, in_timestamp_str, out_timestamp_str = row
    duration = parse_timestamps(in_timestamp_str, out_timestamp_str)
    if duration is not None:
      data.append({"NumberPlate": numberplate, "In Timestamp": in_timestamp_str, "Out Timestamp": out_timestamp_str, "Duration": duration})


parking_durations = [entry["Duration"] for entry in data if entry["Duration"] is not None]
total_entries = len(data)

# Checks for entries with missing durations (potentially incomplete data)
entries_with_missing_duration = len([entry for entry in data if entry["Duration"] is None])
if entries_with_missing_duration > 0:
  print(f"Warning: {entries_with_missing_duration} entries have missing durations (incomplete data?)")

average_duration = sum(parking_durations) / len(parking_durations) if parking_durations else 0
max_duration = max(parking_durations) if parking_durations else 0
min_duration = min(parking_durations) if parking_durations else 0

parking_counts_by_hour = defaultdict(int)
for entry in data:
  if entry["Duration"] is not None:
    hour = entry["In Timestamp"].split(' ')[1].split(':')[0]
    parking_counts_by_hour[int(hour)] += 1



# Visualizations

# 1. Distribution of parking durations
plt.figure(figsize=(8, 6))
sns.histplot(parking_durations, bins='auto', kde=True)
plt.xlabel("Parking Duration (hours)")
plt.ylabel("Number of Vehicles")
plt.title("Distribution of Parking Durations")
plt.grid(True)
plt.show()

# 2. Hourly parking counts
if len(parking_counts_by_hour) > 0:
  plt.figure(figsize=(8, 6))
  sns.barplot(x=parking_counts_by_hour.keys(), y=parking_counts_by_hour.values())
  plt.xlabel("Hour of the Day")
  plt.ylabel("Number of Vehicles Parked")
  plt.title("Hourly Parking Counts")
  plt.xticks(rotation=45)
  plt.grid(True)
  plt.show()

# Prints additional findings
print(f"Total number of entries: {total_entries}")
print(f"Average parking duration: {average_duration:.2f} hours")
print(f"Maximum parking duration: {max_duration:.2f} hours")
print(f"Minimum parking duration: {min_duration:.2f} hours")
