# Excel to CSV and GeoJSON Converter

This Python script converts structured Excel files (with merged headers and body rows) into clean CSV and GeoJSON formats. It is particularly useful for datasets where the first row or multiple rows are used as headers and the data table includes merged cells. The script automatically detects latitude and longitude columns to generate spatial GeoJSON output if applicable.

---

## Features

- **Header cleanup**: Combines multi-row headers into clean, readable column names.
- **Merged cell handling**: Properly fills in values from merged cells using `openpyxl`.
- **Empty row skipping**: Ignores completely empty rows in the body of the spreadsheet.
- **Type conversion**: Attempts numeric conversion for each column.
- **GeoJSON generation**: Automatically detects latitude and longitude columns to produce a `.geojson` file with spatial points.
- **Graceful handling**: Warns about missing or malformed latitude/longitude rows.

---

## Requirements

Install the following Python packages:

```bash
pip install pandas openpyxl numpy
```

---

## Usage

From the command line:

```bash
python script.py <filename.xlsx>
```

For example:

```bash
python excel_to_csv_geojson.py Tsunami_Data_Compilation_TLDR.xlsx
```

### Output:

- `Tsunami_Data_Compilation_TLDR.csv` – cleaned CSV version of your data.
- `Tsunami_Data_Compilation_TLDR.geojson` – GeoJSON file with spatial features (if latitude and longitude columns are present).

---

## How It Works

### Step-by-step Process

1. **Header Parsing**

   - Loads Excel using `pandas` to extract the first row(s) as headers.
   - Merged or multiline headers are forward-filled and combined.
   - Special characters (e.g., units in brackets) are removed.

2. **Body Parsing**

   - Uses `openpyxl` to read body rows, accounting for merged cells using a lookup.
   - Skips rows that are fully empty.
   - Constructs a new DataFrame with cleaned headers and parsed data.

3. **Type Conversion**

   - Tries converting each column to numeric where possible, keeping others as strings.

4. **GeoJSON Output (Optional)**
   - If latitude and longitude columns are detected:
     - Iterates over rows to create GeoJSON features.
     - Formats date columns to `YYYY-MM-DD`.
     - Replaces missing values with empty strings.
     - Writes a valid GeoJSON file with a `FeatureCollection`.

---

## Notes

- The default number of header rows is **1**, but you can change it by modifying `NUM_HEADER_ROWS` at the top of the script.
- Latitude/Longitude detection is case-insensitive (`latitude`, `Latitude`, `LATITUDE`, etc.).
- Merged cells are properly unwrapped and propagated across rows and columns.
- Column names are cleaned for readability (e.g., `"Velocity [m/s]"` → `"Velocity"`).

---

## Example Input Excel

```csv
Evidence Type,Contact Name,Site,Latitude,Longitude
Tsunami inundation,KH-1700,Koprino Harbor,50.50664,-127.839574
Tsunami inundation,NI-1964,Neroutsos Inlet,50.4023,-127.4891
Tsunami inundation,NI-1700,Neroutsos Inlet,50.4023,-127.4891
```

### Output GeoJSON

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-127.839574, 50.50664]
      },
      "properties": {
        "Evidence Type": "Tsunami inundation",
        "Contact Name": "KH-1700",
        "Site": "Koprino Harbor",
        "Latitude": 50.50664,
        "Longitude": -127.839574
      }
    },
    ...
  ]
}
```

---

## 📂 File Naming Convention

- Input: `yourfile.xlsx`
- Output: `yourfile.csv` and `yourfile.geojson`
