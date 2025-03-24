import csv

def read_column(file, column_name):
    with open(file, newline='', encoding='utf-8-sig') as f:  # Handle BOM automatically
        reader = csv.DictReader(f)
        headers = {h.strip(): h for h in reader.fieldnames}  # Normalize headers
        print(f"Headers in {file}: {headers.keys()}")  # Debugging line
        column_name = column_name.strip()  # Ensure we match the stripped version
        if column_name not in headers:
            raise KeyError(f"Column '{column_name}' not found in {file}. Available columns: {list(headers.keys())}")
        return set(row[headers[column_name]].strip().upper() for row in reader if row[headers[column_name]])

def custom_sort_key(item):
    return (item[0].isdigit(), item)

def compare_csv_columns(devices_file, workstations_file, output_file):
    devices_set = read_column(devices_file, 'Hostname')
    workstations_set = read_column(workstations_file, 'Device ID')
    
    # Find differences
    in_devices_not_workstations = sorted(devices_set - workstations_set, key=custom_sort_key)
    in_workstations_not_devices = sorted(workstations_set - devices_set, key=custom_sort_key)
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['In Datto Not Airtable', 'In Airtable Not Datto'])

        max_length = max(len(in_devices_not_workstations), len(in_workstations_not_devices))
        in_devices_not_workstations.extend([""] * (max_length - len(in_devices_not_workstations)))
        in_workstations_not_devices.extend([""] * (max_length - len(in_workstations_not_devices)))
        for d, w in zip(in_devices_not_workstations, in_workstations_not_devices):
            writer.writerow([d, w])
    
    print(f"Comparison complete. Output saved to {output_file}")

# Example usage
compare_csv_columns('input_files/Devices.csv', 'input_files/Workstations.csv', 'Differences.csv')
