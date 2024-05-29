import unittest
from unittest.mock import patch
import sys
sys.path.append('src')
from pdf_parser import PDFParser

class TestPDFParser(unittest.TestCase):
    @patch('pdf_parser.extract_text')
    def test_parse_pdf(self, mock_extract_text):
        # Mock the extract_text function to simulate text extraction
        mock_extract_text.return_value = "The total amount of funds requested is $5,000. EFC’s Call for Letters of Intent process is on December 31st, 2021."

        parser = PDFParser()
        parsed_data = parser.parse_pdf('path_to_pdf_file.pdf')

        self.assertTrue(any(amount in parsed_data['Max Funding'] for amount in ['$5,000', '5000']))
        self.assertTrue(any(date in parsed_data['Due Date'] for date in ['December 31st, 2021', 'Dec 31, 2021']))

if __name__ == '__main__':
    unittest.main()