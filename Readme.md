# Sigma Connect Take Home Assignment
This project solves the basic situtation outlined below:
Your company ingests customer transaction data from different sources each day.
The data arrives in different formats (CSV, JSON, XML), contains inconsistencies
and errors, and uses multiple currencies.

## Features
This project reads from three source(JSON, CSV, XML) then combines the common fields from these sources into two output CSV files. One that only contains records that have no suspicious data present and the file contains all the data that contains suspicious data.
- Attemps to load franfurter API for accurate currency conversion
- Adds flag column to suspicious data CSV that clear shows the reasons as to why a record is determined to be suspicious e.g. negative amounts for transactions
- Handles inconsistent data by forcing a naming convetion onto the dataframes generated from the sources e.g. altering the 'id' column from the JSON source into 'transaction_id' to match other sources
- Handles inconsisten data entry in records e.g. In the XML file the data and time are store inconsistently this project handles these inconsistencies before spliting the values into date and time
- This project also makes sure that the time and date are entered correctly after the split e.g. if the date was entered incorrectly but the time was correct in format the project would only flag the date and vice versus however if both are missing or incorrect the project will flag both
- This project includes a testscript used to test function from the main script
- The all currency is standardised to USD using live rates from  [Frankfurter API](https://www.frankfurter.dev/) this however is only performed on the cleaned dataframe as to save on computational resources and time
- Saves the final outputs into two CSV files for ease of use by analyst

## Assumptions
- I assumed this project was for small to medium source files as if large scale source are to be used the way data is read should be adjusted to account for the scale e.g. loading smaller batches into memory and processing those before flushing memory and then loading the next chunk.
- I assumed that although there is an inconsistent format between different sources. that data from a specific source would maintain the same format e.g. a JSON file will have the same format as the JSON file provided.
- I assumed that dat unique to a single source would not be needed in the combined output hence certain fields were dropped in the final output e.g. the 'meta' field from the JSON file
- I assumed saving the results as two CSV files would be sufficient as there was no link or mention of a SQL database 
- I assumed that those who will run this project have python installed on their computer
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

