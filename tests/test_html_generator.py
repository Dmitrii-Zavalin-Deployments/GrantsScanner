'''
import unittest
from src.html_generator import HTMLGenerator
import os
import json

class TestHTMLGenerator(unittest.TestCase):
    def setUp(self):
        # Set up test data
        self.test_data = [
            {
                "Country": "Testland",
                "MaxFunding": "10000",
                "DueDate": "2024-12-31",
                "Requirements": "Test requirements",
                "SubmissionItems": "Test items",
                "PDFLink": "http://example.com/test.pdf",
                "Query": "test query"
            }
        ]
        self.test_data_file = 'test_grants.json'
        self.test_output_file = 'test_grants.html'

        # Write test data to a file
        with open(self.test_data_file, 'w') as file:
            json.dump(self.test_data, file)

    def test_generate_html(self):
        # Initialize HTMLGenerator with test data file
        html_generator = HTMLGenerator(self.test_data_file)
        
        # Generate HTML
        html_generator.generate_html(self.test_output_file)

        # Check if the output file was created
        self.assertTrue(os.path.exists(self.test_output_file))

    def tearDown(self):
        # Clean up test files
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
        if os.path.exists(self.test_output_file):
            os.remove(self.test_output_file)

if __name__ == '__main__':
    unittest.main()
'''