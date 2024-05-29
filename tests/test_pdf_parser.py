import unittest
from unittest.mock import patch
from src.pdf_parser import PDFParser

class TestPDFParser(unittest.TestCase):
    @patch('pdf_parser.extract_text')
    def test_parse_pdf(self, mock_extract_text):
        # Mock the extract_text function to simulate text extraction
        mock_extract_text.return_value = "The maximum funding is $5000. Application deadline: Dec 31, 2021."

        parser = PDFParser()
        parsed_data = parser.parse_pdf('path_to_pdf_file.pdf')

        self.assertIn('The maximum funding is $5000', parsed_data['Max Funding'])
        self.assertIn('Application deadline: Dec 31, 2021', parsed_data['Due Date'])

if __name__ == '__main__':
    unittest.main()
