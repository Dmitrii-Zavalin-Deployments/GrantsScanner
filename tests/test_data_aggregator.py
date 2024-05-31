import unittest
from unittest.mock import patch, mock_open, call, MagicMock
import json
from src.data_aggregator import DataAggregator
import logging
from io import StringIO

class TestDataAggregator(unittest.TestCase):

    def setUp(self):
        self.aggregator = DataAggregator('test_grants.json')

    @patch('os.path.exists')
    @patch('os.path.getsize')
    def test_read_grants_data_empty_file(self, mock_getsize, mock_exists):
        # Test reading from an empty grants file
        mock_exists.return_value = True
        mock_getsize.return_value = 0
        self.assertEqual(self.aggregator.read_grants_data(), {})

    @patch('builtins.open', new_callable=mock_open, read_data='{"0": {"link": "http://example.com"}}')
    def test_read_grants_data_non_empty_file(self, mock_file):
        # Test reading from a non-empty grants file
        data = self.aggregator.read_grants_data()
        self.assertIn({}, data)
        self.assertEqual(data['0']['link'], 'http://example.com')

    @patch('builtins.open', new_callable=mock_open)
    def test_write_grants_data(self, mock_file):
        # Test writing data to the grants file
        test_data = {'1': {'link': 'http://example.com/new'}}
        self.aggregator.write_grants_data(test_data)
        mock_file_handle = mock_file()
        expected_json = json.dumps(test_data, indent=4)
        actual_calls = ''.join(call_args[0][0] for call_args in mock_file_handle.write.call_args_list)
        self.assertEqual(expected_json, actual_calls)

    @patch('src.data_aggregator.DataAggregator.read_grants_data')
    @patch('src.data_aggregator.DataAggregator.write_grants_data')
    def test_add_grant_data_new_entry(self, mock_write, mock_read):
        # Test adding a new grant entry
        mock_read.return_value = {}
        query_data = {"name": "Test Grant", "query": "Test Query"}
        pdf_url = "http://example.com/new_grant.pdf"
        parsed_data = {"Funds": "5000", "Dates": "2024-01-01 to 2024-12-31", "Requirements": "None", "Documents": "None", "Summary": "Test Summary"}
        self.aggregator.add_grant_data(query_data, pdf_url, parsed_data)
        mock_write.assert_called_once()

    def test_add_grant_data_existing_entry(self):
        # Set up the logging to capture output for testing
        log_capture_string = StringIO()
        ch = logging.StreamHandler(log_capture_string)
        ch.setLevel(logging.INFO)
        logger = logging.getLogger()
        logger.addHandler(ch)

        # Set up mock data and call the method
        aggregator = DataAggregator('test_grants.json')
        query_data = {"name": "Existing Grant", "query": "Existing Query"}
        pdf_url = "http://example.com/existing_grant.pdf"
        parsed_data = {"Funds": "10000", "Dates": "2024-01-01 to 2024-12-31", "Requirements": "None", "Documents": "None", "Summary": "Existing Summary"}

        with patch('src.data_aggregator.DataAggregator.read_grants_data', return_value={'0': {'link': pdf_url}}):
            aggregator.add_grant_data(query_data, pdf_url, parsed_data)

        # Check the log output
        self.assertIn("The grant with url: http://example.com/existing_grant.pdf is already in the system.", log_capture_string.readline())

        # Remove the log handler after the test
        logger.removeHandler(ch)

if __name__ == '__main__':
    unittest.main()
