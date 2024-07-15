import csv

def match_number_plates(file1_path, file2_path, output_path=None):

  # Load CSV files into sets for efficient membership checks
  plate_set1 = set()
  with open(file1_path, 'r') as file1:
    reader = csv.reader(file1)
    header = next(reader)  # Skip header row if present
    for row in reader:
      # Assuming "NumberPlate" is the column name (adjust if needed)
      number_plate = row[header.index("NumberPlate")].upper()  # Convert to uppercase for case-insensitive matching
      plate_set1.add(number_plate)

  plate_set2 = set()
  with open(file2_path, 'r') as file2:
    reader = csv.reader(file2)
    header = next(reader)  # Skip header row if present
    for row in reader:
      number_plate = row[header.index("NumberPlate")].upper()  # Convert to uppercase for case-insensitive matching
      plate_set2.add(number_plate)

  # Find common plates
  common_plates = plate_set1.intersection(plate_set2)

  # Display or write common plates
  if output_path:
    with open(output_path, 'w', newline='') as output_file:
      writer = csv.writer(output_file)
      writer.writerow(["Common Number Plates"])  # Write header if desired
      for plate in common_plates:
        writer.writerow([plate])
  else:
    print("Common Number Plates:")
    for plate in common_plates:
      print(plate)

# Example usage
file1 = "approved_vehicles.csv"
file2 = "parking_entries_exits.csv"
output_file = "common_plates.csv"  # Optional output file path

match_number_plates(file1, file2, output_file)  # Write common plates to output.csv
match_number_plates(file1, file2)  # Print common plates to console
