# Sigma Connect Take Home Assignment
This project solves the basic situation outlined below:
The company ingests customer transaction data from different sources each day.
The data arrives in different formats (CSV, JSON, XML), containing inconsistencies and errors, and uses multiple currencies.

## Features
This project reads from three sources (JSON, CSV, XML) then combines the common fields from these sources into two output CSV files:
- One file that only contains records with no suspicious data present.
- One file that contains all data with suspicious values. <br>
Key features:
- Attempts to load the Frankfurter API for accurate currency conversion.
- Adds a flag column to the suspicious data CSV that clearly shows the reasons why a record is determined to be suspicious (e.g., negative transaction amounts).
- Handles inconsistent data by enforcing a naming convention on the DataFrames generated from the sources (e.g., renaming the id column from the JSON source to transaction_id to match other sources).
- Handles inconsistent data entry in records (e.g., in the XML file the date and time are stored inconsistently; this project standardizes them before splitting values into date and time).
- Ensures that the time and date are entered correctly after splitting (e.g., if the date was incorrect but the time was correct, the project only flags the date, and vice versa. If both are missing or incorrect, the project flags both).
- Includes a unit testing script to validate functions from the main script.
- All currencies are standardized to USD using live rates from the Frankfurter API(https://www.frankfurter.dev/).
This is only performed on the cleaned DataFrame to save computational resources and time.
- Saves the final outputs into two CSV files for ease of use by analysts as mentioned above.

## Assumptions
- The project is intended for small to medium source files. For large-scale sources, the data reading method should be adjusted (e.g., loading smaller batches into memory, processing them, then flushing memory before loading the next chunk).
- Although formats are inconsistent across different sources, data from the same source is assumed to be consistent (e.g., all JSON files will share the same format as the provided JSON file).
- Data unique to a single source is not needed in the combined output; these fields are dropped in the final output (e.g., the meta field from the JSON file).
- Saving results as two CSV files is sufficient, since no SQL database was specified or required.
- Users running this project are assumed to have Python installed on their computer.
## Installation

Clone the repository and install dependencies:
```bash
git clone git@github.com:Bernhardt-Steyn/DataCleanerSigma.git
cd DataCleanerSigma

# (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# Install requirements
pip install -r requirements.txt

# All provide data sources are located in the data directory. New sources should be stored in this directory as well. The path flags will also need to be altered for the project to read new data sources.

# Run program
python3 ./src/script.py

# Run testscript
python3 ./test/test_script.py
