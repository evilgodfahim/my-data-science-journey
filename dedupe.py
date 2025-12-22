import csv

# Input and output file paths
input_file = 'kimshim.txt'
output_file = 'kimshim_deduplicated.txt'

# Track seen fronts and store unique rows
seen_fronts = set()
unique_rows = []

# Read the CSV file
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    
    # Read header
    header = next(reader)
    unique_rows.append(header)
    
    # Process each row
    for row in reader:
        if len(row) >= 2:
            front = row[0]
            
            # Only keep first occurrence of each front
            if front not in seen_fronts:
                seen_fronts.add(front)
                unique_rows.append(row)

# Write to output file with preserved CSV format
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(unique_rows)

print(f"Original rows: {len(unique_rows) - 1 + len(seen_fronts)}")
print(f"Unique rows: {len(unique_rows) - 1}")
print(f"Duplicates removed: {len(seen_fronts) - (len(unique_rows) - 1)}")
print(f"Output saved to: {output_file}")
