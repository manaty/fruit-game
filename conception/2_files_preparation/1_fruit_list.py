import csv
import re

# File paths
input_file = '../1_content/4_Properties.md'
output_file = '1.2_fruit_properties.csv'

# Regex patterns to capture fruit properties
fruit_section_pattern = re.compile(r'#### \*\*(.*?)\*\*')
property_pattern = re.compile(r'- \*\*(.*?):\*\* (.*)')

# Dictionary to store fruit data
fruits_data = []

# Open the markdown file for reading
with open(input_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()

current_fruit = None
fruit_details = {}

# Parse each line
for line in lines:
    fruit_section_match = fruit_section_pattern.search(line)
    property_match = property_pattern.search(line)

    # If a new fruit section is detected
    if fruit_section_match:
        # If there is a current fruit, append its details before starting a new one
        if current_fruit:
            fruits_data.append(fruit_details)

        # Initialize new fruit details
        current_fruit = fruit_section_match.group(1)
        fruit_details = {'Name': current_fruit}

    # If a property is detected, add it to the current fruit's details
    elif property_match and current_fruit:
        property_name = property_match.group(1)
        property_value = property_match.group(2)
        fruit_details[property_name] = property_value

# Append the last fruit details after reading all lines
if current_fruit:
    fruits_data.append(fruit_details)

# Define the column names
column_names = [
    'Name', 'Family', 'Color(s)', 'Place of Origin', 'Countries Where It Grows',
    'Importance in Industry', 'Historical Significance', 'Nutritional Benefits',
    'Medicinal Uses', 'Interesting Chemicals'
]

# Write the data to a CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=column_names)
    writer.writeheader()
    writer.writerows(fruits_data)

print(f"CSV file created: {output_file}")
