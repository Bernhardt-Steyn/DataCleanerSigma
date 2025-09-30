# Imports
import unittest
import sys
import os
import pandas as pd

# Get the parent directory of the current file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

# Imports script to be tested
from src import script


# Testing class
class TestMain(unittest.TestCase):
    # Tests how script handles empty path to JSON file 
    # if handled correctly script will return -1
    def test_JSON_File_EMPTY(self):
        result = script.open_json('')
        self.assertEqual(result, -1)
    # Tests how script handles empty path to CSV file
    # if handled correctly script will return -1
    def test_CSV_File_EMPTY(self):
        result = script.open_csv('')
        self.assertEqual(result, -1)
    # Tests how script handles empty path to XML file
    # if handled correctly script will return -1
    def test_XML_File_EMPTY(self):
        result = script.open_xml('')
        self.assertEqual(result, -1)

    # Tests how script handles valid path to JSON file
    # if handled correctly script will return a dataframe
    def test_JSON_File(self):
        result = script.open_json(script.JSON_PATH)
        self.assertIsInstance(result, pd.DataFrame)
    # Tests how script handles valid path to CSV file
    # if handled correctly script will return a dataframe
    def test_CSV_File(self):
        result = script.open_csv(script.CSV_PATH)
        self.assertIsInstance(result, pd.DataFrame)
    # Tests how script handles valid path to XML file
    # if handled correctly script will return a dataframe
    def test_XML_File(self):
        result = script.open_xml(script.XML_PATH)
        self.assertIsInstance(result, pd.DataFrame)


    # Tests how flag method handles a invalid customer id
    # Correct output return the "'Invalid Customer ID'" flag
    def test_FLAG_CUSTOMER_ID_INVALID(self):
        row = {"customer_id" : "C--1", "transaction_id" : "S-A_1001", "date" : "2011-02-04", "time" : r"07:14:03\+00:00", "amount" : 300, "currency" : "USD", "payment_method" : "card", "source_id" : "online"}
        result = script.flag(row)
        self.assertIn('Invalid Customer ID', result)
    # Tests how flag method handles a invalid transaction id
    # Correct output return the "'Invalid Transaction ID'" flag
    def test_FLAG_TRANSACTION_ID_INVALID(self):
        row = {"customer_id" : "C-900", "transaction_id" : None, "date" : "2011-02-04", "time" : r"07:14:03\+00:00", "amount" : 300, "currency" : "USD", "payment_method" : "card", "source_id" : "online"}
        result = script.flag(row)
        self.assertIn('Invalid Transaction ID', result)
    # Tests how flag method handles a invalid date
    # Correct output return the "'Invalid Date Value'" flag
    def test_FLAG_DATE_INVALID(self):
        row = {"customer_id" : "C-900", "transaction_id" : "S-A_1001", "date" : "_", "time" : r"07:14:03+00:00", "amount" : 300, "currency" : "USD", "payment_method" : "card", "source_id" : "online"}
        result = script.flag(row)
        self.assertIn('Invalid Date Value', result)
    # Tests how flag method handles a invalid date
    # Correct output return the "'Invalid Date Value'" flag
    def test_FLAG_DATE_INVALID_format01(self):
        row = {"customer_id" : "C-900", "transaction_id" : "S-A_1001", "date" : "2011-0204", "time" : r"07:14:03+00:00", "amount" : 300, "currency" : "USD", "payment_method" : "card", "source_id" : "online"}
        result = script.flag(row)
        self.assertIn('Invalid Date Value', result)
    # Tests how flag method handles a invalid date
    # Correct output return the "'Invalid Date Value'" flag
    def test_FLAG_DATE_INVALID_format02(self):
        row = {"customer_id" : "C-900", "transaction_id" : "S-A_1001", "date" : "2011-02-04:", "time" : r"07:14:03+00:00", "amount" : 300, "currency" : "USD", "payment_method" : "card", "source_id" : "online"}
        result = script.flag(row)
        self.assertIn('Invalid Date Value', result)
    # Tests how flag method handles a time date
    # Correct output return the "'Invalid Time Value'" flag
    def test_FLAG_TIME_INVALID(self):
        row = {"customer_id" : "C-900", "transaction_id" : "S-A_1001", "date" : "2011-02-04", "time" : pd.NA, "amount" : 300, "currency" : "USD", "payment_method" : "card", "source_id" : "online"}
        result = script.flag(row)
        self.assertIn('Invalid Time Value', result)
    # Tests how flag method handles a time date
    # Correct output return the "'Invalid Time Value'" flag
    def test_FLAG_TIME_INVALID_Format01(self):
        row = {"customer_id" : "C-900", "transaction_id" : "S-A_1001", "date" : "2011-02-04", "time" : r"07:14:0300:00", "amount" : 300, "currency" : "USD", "payment_method" : "card", "source_id" : "online"}
        result = script.flag(row)
        self.assertIn('Invalid Time Value', result)
    # Tests how flag method handles a time date
    # Correct output return the "'Invalid Time Value'" flag
    def test_FLAG_TIME_INVALID_format02(self):
        row = {"customer_id" : "C-900", "transaction_id" : "S-A_1001", "date" : "2011-02-04", "time" : r"07:1403\+00:00", "amount" : 300, "currency" : "USD", "payment_method" : "card", "source_id" : "online"}
        result = script.flag(row)
        self.assertIn('Invalid Time Value', result)
    # Tests how flag method handles a invalid amount
    # Correct output return the "'Invalid Amount'" flag
    def test_FLAG_AMOUNT_INVALID(self):
        row = {"customer_id" : "C-900", "transaction_id" : "S-A_1001", "date" : "2011-02-04", "time" : r"07:14:03\+00:00", "amount" : -1, "currency" : "USD", "payment_method" : "card", "source_id" : "online"}
        result = script.flag(row)
        self.assertIn('Invalid Amount', result)
    # Tests how flag method handles a invalid currency
    # Correct output return the "'Invalid Currency'" flag
    def test_FLAG_CURRENCY_INVALID(self):
        row = {"customer_id" : "C-900", "transaction_id" : "S-A_1001", "date" : "2011-02-04", "time" : r"07:14:03\+00:00", "amount" : 300, "currency" : "USDEUR", "payment_method" : "card", "source_id" : "online"}
        result = script.flag(row)
        self.assertIn('Invalid Currency', result)
    # Tests how flag method handles a invalid payment method
    # Correct output return the "'Invalid Payment Method'" flag
    def test_FLAG_PAYMENT_METHOD_INVALID(self):
        row = {"customer_id" : "C-900", "transaction_id" : "S-A_1001", "date" : "2011-02-04", "time" : r"07:14:03\+00:00", "amount" : 300, "currency" : "USD", "payment_method" : None, "source_id" : "online"}
        result = script.flag(row)
        self.assertIn('Invalid Payment Method', result)
    # Tests how flag method handles a invalid source id
    # Correct output return the "'Invalid Source ID'" flag
    def test_FLAG_SOURCE_INVALID(self):
        row = {"customer_id" : "C-900", "transaction_id" : "S-A_1001", "date" : "2011-02-04", "time" : r"07:14:03\+00:00", "amount" : 300, "currency" : "USD", "payment_method" : "card", "source_id" : None}
        result = script.flag(row)
        self.assertIn('Invalid Source ID', result)
    # Tests how flag method handles a valid input
    # Correct output returns a empty list with no flags
    def test_FLAG_VALID(self):
        row = {"customer_id" : "C-900", "transaction_id" : "S-A_1001", "date" : "2011-02-04", "time" : r"07:14:03\+00:00", "amount" : 300, "currency" : "USD", "payment_method" : "card", "source_id" : "online"}
        result = script.flag(row)
        self.assertNotIn('Invalid Customer ID', result)
        self.assertNotIn('Invalid Transaction ID', result)
        self.assertNotIn('Invalid Date Value', result)
        self.assertNotIn('Invalid Time Value', result)
        self.assertNotIn('Invalid Amount', result)
        self.assertNotIn('Invalid Currency', result)
        self.assertNotIn('Invalid Payment Method', result)
        self.assertNotIn('Invalid Source ID', result)

if __name__ == "__main__":
    unittest.main()
