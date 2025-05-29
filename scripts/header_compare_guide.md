# Header Compare Utility

This script (`header_compare.py`) is designed to compare the column headers of a data CSV file with the first column of a separate description CSV file. It identifies mismatches, updates the description file, and generates a corresponding JSON description file.

---

## Features

- Compares column headers between two CSV files.
- Highlights matches and mismatches.
- Outputs a comparison results CSV file.
- Updates the description CSV with the latest headers from the data file.
- Generates a well-structured JSON metadata file from the updated description file.

---

## Requirements

Install dependencies using:

```bash
pip install pandas
```

---

## Usage

```bash
python header_compare.py <data_file.csv> <description_file.csv>
```

### Example:

```bash
python header_compare.py Tsunami_Data_Compilation_TLDR.csv Tsunami_Data_Compilation_cell_descriptions.csv
```

---

## Description File Format

The description CSV should be structured as follows:

```csv
Cell Name,Show/No-show,Cell Description
Evidence Type,Yes,Brief description on the type of paleoseismic evidence
Contact Name,Yes,A uniquely indentified name for each interpreted paleoseismic event. Contact names are based largely on those published in primary literature.
Site,Yes,The geographic name for each site based largely on those published in primary literature.
...
```

## Output

3. **`Tsunami_Data_Compilation_cell_descriptions.json`**  
    A JSON metadata file structured as follows. The headers from the data file with `display` (display the row or not) and `description` (detailed description of the cell header) attributes. :

   ```json
   {
    "Evidence Type": {
        "display": "Yes",
        "description": "Brief description on the type of paleoseismic evidence"
    },
    "Contact Name": {
        "display": "Yes",
        "description": "A uniquely indentified name for each interpreted paleoseismic event. Contact names are based largely on those published in primary literature."
    },
    "Site": {
        "display": "Yes",
        "description": "The geographic name for each site based largely on those published in primary literature."
    },
    "Latitude": {
        "display": "Yes",
        "description": "A general latitude for the site in decimal degrees."
    },

       ...
   }
   ```

---

## Notes

- The code assume the row of the description file are in the same order as the columns of the corresponding data file.
