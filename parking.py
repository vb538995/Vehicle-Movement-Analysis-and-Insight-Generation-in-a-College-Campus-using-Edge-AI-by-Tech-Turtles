import csv
from datetime import datetime

def match_and_assign_parking(file1, file2, output_file, parking_data_file):

  parking_data = {"A": 50, "B": 50, "C": 50, "D": 50, "Visitor": 50}
  assigned_parking = {}
  unmatched_plates = set()

  # Read approved vehicles data
  with open(file2, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
      numberplate, parking_lot = row[0], row[1]
      assigned_parking[numberplate] = parking_lot

  # Read parking entries
  with open(file1, 'r') as csvfile:
    reader = csv.reader(csvfile)
    timestamp = None
    for row in reader:
      if len(row) < 2:
          print(f"Warning: Invalid row in 'parking_entries_exits.csv' - Missing columns.")
          continue

      numberplate1, timestamp_str = row[0], row[1]
      unmatched_plates.add(numberplate1)  # Initially all plates are unmatched

      try:
          timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")  # Assuming timestamp format
      except ValueError:
          print(f"Warning: Invalid timestamp format for '{numberplate}' in 'parking_entries_exits.csv'.")
          continue

      # Check for assigned parking lot
      if numberplate1 in assigned_parking:
        parking_lot = assigned_parking[numberplate1]
        if parking_data[parking_lot] > 0:
          parking_data[parking_lot] -= 1
          unmatched_plates.remove(numberplate1)

  # Writing assigned parking results
  with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Number Plate", "Assigned Parking Lot", "Available Slots", "Timestamp"])
    for numberplate1, parking_lot in assigned_parking.items():
      if numberplate1 not in unmatched_plates:
        available_slots = parking_data[parking_lot]
        writer.writerow([numberplate1, parking_lot, available_slots, timestamp])

  # Writing the remaining parking slots data
  with open(parking_data_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Parking Lot Type", "Available Slots", "Timestamp"])

    writer.writerow([parking_lot, slots, timestamp] for parking_lot, slots in parking_data.items())


file1 = "parking_entries_exits.csv"
file2 = "approved_vehicles.csv"
output_file = "assigned_parking.csv"
parking_data_file = "parking_data.csv"

match_and_assign_parking(file1, file2, output_file, parking_data_file)

print(f"Matching and parking lot assignment completed. Results saved to '{output_file}'.")
print(f"Parking data saved to '{parking_data_file}'.")
