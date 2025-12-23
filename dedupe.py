import csv
import os

# Input and output file paths
input_file = 'oneworde.txt'
output_file = 'oneworde_temp.txt'

# Track seen fronts and store unique rows
seen_fronts = set()
unique_rows = []

# Read the CSV file
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    
    # Process each row (no header)
    for row in reader:
        if len(row) >= 2:
            front = row[0]
            
            # Only keep first occurrence of each front
            if front not in seen_fronts:
                seen_fronts.add(front)
                unique_rows.append(row)

# Write to temp file
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(unique_rows)

print(f"Total rows processed: {len(seen_fronts)}")
print(f"Unique rows kept: {len(unique_rows)}")
print(f"Duplicates removed: {len(seen_fronts) - len(unique_rows)}")

# Replace original file with deduplicated version
os.replace(output_file, input_file)
print(f"Successfully deduplicated {input_file}")
