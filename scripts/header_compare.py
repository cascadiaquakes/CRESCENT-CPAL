import pandas as pd
import argparse
import json

def compare_csv_headers(data_file, description_file):
    # Load the data file and get column headers
    data_df = pd.read_csv(data_file)
    data_columns = list(data_df.columns)
    
    # Load the description file and get the first column values, ignoring the first row
    description_df = pd.read_csv(description_file, header=None)
    header_row = description_df.iloc[0]  # Preserve the header row
    description_df = description_df.iloc[1:].reset_index(drop=True)  # Remove the first row
    description_values = list(description_df.iloc[:, 0])  # First column of description file
    
    # Ensure both lists have the same length
    max_length = max(len(data_columns), len(description_values))
    data_columns.extend([None] * (max_length - len(data_columns)))
    description_values.extend([None] * (max_length - len(description_values)))
    
    # Compare values one by one
    results = []
    for data_col, desc_val in zip(data_columns, description_values):
        match_status = "Match" if data_col == desc_val else "No Match"
        results.append([data_col, desc_val, match_status])
    
    # Convert results to DataFrame
    results_df = pd.DataFrame(results, columns=["Data File Column", "Description File Value", "Match Status"])
    
    # Print results
    print(results_df.to_string(index=False))
    
    # Save results to a CSV file
    results_df.to_csv("comparison_results.csv", index=False)
    print("Comparison results saved to comparison_results.csv")
    
    # Update description file with new first column values from data file's column headers
    description_df.iloc[:, 0] = data_columns[:len(description_df)]  # Replace first column with corresponding column headers
    updated_description_df = pd.concat([header_row.to_frame().T, description_df], ignore_index=True)  # Re-add header row
    updated_description_df.to_csv("updated_description.csv", index=False, header=False)
    print("Updated description file saved to updated_description.csv")
    
    # Convert updated description file to JSON
    json_data = {}
    for _, row in description_df.iterrows():
        key = row[0]  # Use updated first column value as key
        json_data[key] = {
            "display": row[1],
            "description": row[2]
        }
    
    with open(description_file.replace(".csv",".json"), "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4)
    print("JSON file saved as description.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare CSV column headers with description file and generate JSON")
    parser.add_argument("data_file", help="Path to the data CSV file")
    parser.add_argument("description_file", help="Path to the description CSV file")
    args = parser.parse_args()
    
    compare_csv_headers(args.data_file, args.description_file)

