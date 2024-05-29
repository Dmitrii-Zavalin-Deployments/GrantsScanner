import unittest
from unittest.mock import patch
from src.pdf_parser import PDFParser

class TestPDFParser(unittest.TestCase):
    @patch('src.pdf_parser.extract_text')
    def test_parse_pdf_non_pdf_file(self, mock_extract_text):
        # Simulate an exception being raised by extract_text
        mock_extract_text.side_effect = Exception("File is not a PDF")

        parser = PDFParser()
        parsed_data = parser.parse_pdf('dummy_path_to_non_pdf_file')

        # Assertions to check if the correct data is returned for a non-PDF file
        self.assertEqual(parsed_data, {'Max Funding': 'Not found', 'Due Date': 'Not found', 'Requirements': 'Not found', 'Submission Items': 'Not found'})
    
    @patch('src.pdf_parser.extract_text')
    def test_parse_pdf(self, mock_extract_text):
        # Mock the extract_text function to simulate text extraction
        mock_extract_text.return_value = "The maximum funding available is $5,000. The application deadline is Dec 31, 2024."

        parser = PDFParser()
        parsed_data = parser.parse_pdf('dummy_path_to_pdf_file.pdf')

        # Print statement to check the content of 'Max Funding'
        print(f"Max Funding: {parsed_data['Max Funding']}")

        # Assertions to check if the test passes
        self.assertIn('$5,000', parsed_data['Max Funding'])
        self.assertIn('Dec 31, 2024', parsed_data['Due Date'])

if __name__ == '__main__':
    unittest.main()
