import pandas as pd

def main():
    from dataprocessor import revit_data_processing, process_epd_data

    revit_data_processing()
    process_epd_data()

    # Read the CSV files with correct delimiter and decimal
    df1 = pd.read_csv('output_files/Concrete.csv', delimiter=';', decimal=',')
    df2 = pd.read_csv('output_files/Steel.csv', delimiter=';', decimal=',')
    df3 = pd.read_csv('output_files/Wood.csv', delimiter=';', decimal=',')

    # Revit data file
    revit_data = pd.read_csv('revit_processed.csv', delimiter=';', decimal=',')

    # Create a dictionary to map phase names to column names in revit_data
    phase_mapping = {
        'A1-A3': 'A1-A3',
        'A4': 'A4',
        'A5': 'A5',
        'B1': 'B1',
        'B2': 'B2',
        'B3': 'B3',
        'B4': 'B4',
        'B5': 'B5',
        'B6': 'B6',
        'B7': 'B7',
        'C1': 'C1',
        'C2': 'C2',
        'C3': 'C3',
        'C4': 'C4',
        'D': 'D'
    }

    # List to store the results for each row
    individual_results = []

    # Loop through the rows of revit_data
    for index, row in revit_data.iterrows():
        volume = row['Volume']
        material = row['Material']

        # Determine the correct DataFrame based on material
        if material == 'Concrete':
            df = df1
        elif material == 'Wood':
            df = df3
        elif material == 'Steel':
            df = df2
        else:
            continue

        # Dictionary to store results for the current row
        row_result = {phase: 0 for phase in phase_mapping}
        row_result['Material'] = material
        row_result['Volume'] = volume
        row_result['Source'] = df.at[0, 'Source']  # Add source information

        # Calculations for each phase
        for phase in phase_mapping:
            value = df.at[0, phase]
            row_result[phase] = float(value) * volume

        individual_results.append(row_result)

    # DataFrame for individual results
    individual_results_df = pd.DataFrame(individual_results)

    # Calculate total results
    total_results = individual_results_df.sum(numeric_only=True)
    total_results['Source'] = [df1.at[0, 'Source'], df2.at[0, 'Source'], df3.at[0, 'Source']]

    # DataFrame for total results
    total_results_df = pd.DataFrame([total_results])

    # Save the tables to HTML files
    individual_results_df.to_html('individual_results.html', index=False)
    total_results_df.to_html('total_results.html', index=False)

    print("Tables saved as HTML files.")

if __name__ == "__main__":
    main()