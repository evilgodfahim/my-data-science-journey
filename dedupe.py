import csv

# Input and output file paths
input_file = 'oneworde.txt'
output_file = 'oneworde_deduplicated.txt'

# Track seen fronts and store unique rows
seen_fronts = set()
unique_rows = []

# Read the CSV file
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    
    # Process each row (no header in this format)
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

print(f"Total rows processed: {len(seen_fronts)}")
print(f"Unique rows kept: {len(unique_rows)}")
print(f"Duplicates removed: {len(seen_fronts) - len(unique_rows)}")
print(f"Output saved to: {output_file}")
