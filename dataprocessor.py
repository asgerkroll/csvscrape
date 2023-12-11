import csv
import os
import pandas as pd

def process_epd_data():
    # Create a folder to store the output files
    output_folder = 'output_files'
    os.makedirs(output_folder, exist_ok=True)

    # Read the input CSV file
    with open('EPD_Data.CSV', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        # Create separate output files for each material
        material_files = {}
        for row in reader:
            material = row['Material']
            if material not in material_files:
                material_file = open(os.path.join(output_folder, f'{material}.csv'), 'w', newline='')
                material_writer = csv.DictWriter(material_file, fieldnames=reader.fieldnames, delimiter=';')
                material_writer.writeheader()
                material_files[material] = material_file, material_writer

            material_writer = material_files[material][1]
            material_writer.writerow(row)

    # Close all material files
    for _, (material_file, _) in material_files.items():
        material_file.close()
process_epd_data()

def revit_data_processing():
    # Read the CSV file with the specified delimiter and header names
    df = pd.read_csv('Project_data.csv', delimiter=';', skiprows=0)

    # Remove " m³" from the 'Material: Volume' column and replace "," with "."
    df['Material: Volume'] = df['Material: Volume'].str.replace(' m³', '').str.replace(',', '.', regex=False)

    # Rename columns
    df.columns = ['Volume', 'Material']

    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')

    # Replace values in the 'Material' column with 'Concrete' for all rows except the first
    df.loc[0:, 'Material'] = 'Concrete'

    # Filter rows where the 'Volume' column is not empty
    df = df[df['Volume'].notna()]

    # Save the modified DataFrame to a new CSV file
    df.to_csv('revit_processed.csv', index=False, sep=';')

revit_data_processing()
