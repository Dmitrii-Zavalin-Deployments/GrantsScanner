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

        # Assertions to check if the test passes
        self.assertIn('$5,000', parsed_data['Max Funding'])
        self.assertIn('Dec 31, 2024', parsed_data['Due Date'])
        
    @patch('src.pdf_parser.extract_text')
    def test_max_funding_simple(self, mock_extract_text):
        mock_extract_text.return_value = "The maximum funding available is $5,000."
        parser = PDFParser()
        parsed_data = parser.parse_pdf('dummy_path_to_pdf_file.pdf')
        self.assertIn('$5,000', parsed_data['Max Funding'])

    @patch('src.pdf_parser.extract_text')
    def test_due_date_simple(self, mock_extract_text):
        mock_extract_text.return_value = "The application deadline is Dec 31, 2024."
        parser = PDFParser()
        parsed_data = parser.parse_pdf('dummy_path_to_pdf_file.pdf')
        self.assertIn('Dec 31, 2024', parsed_data['Due Date'])

    @patch('src.pdf_parser.extract_text')
    def test_max_funding_complex(self, mock_extract_text):
        mock_extract_text.return_value = "Applicants may request up to $10,000, though most awards are between $2,000 and $5,000."
        parser = PDFParser()
        parsed_data = parser.parse_pdf('dummy_path_to_pdf_file.pdf')
        self.assertIn('up to $10,000', parsed_data['Max Funding'])

    @patch('src.pdf_parser.extract_text')
    def test_due_date_variations(self, mock_extract_text):
        mock_extract_text.return_value = "All submissions must be received by the 31st of December, 2024."
        parser = PDFParser()
        parsed_data = parser.parse_pdf('dummy_path_to_pdf_file.pdf')
        self.assertIn('31st of December, 2024', parsed_data['Due Date'])

    @patch('src.pdf_parser.extract_text')
    def test_max_funding_range(self, mock_extract_text):
        mock_extract_text.return_value = "Funding can range from $1,000 to $10,000 depending on project scope."
        parser = PDFParser()
        parsed_data = parser.parse_pdf('dummy_path_to_pdf_file.pdf')
        self.assertIn('from $1,000 to $10,000', parsed_data['Max Funding'])

    @patch('src.pdf_parser.extract_text')
    def test_due_date_ambiguous(self, mock_extract_text):
        mock_extract_text.return_value = "The final date to submit applications is at the end of the year."
        parser = PDFParser()
        parsed_data = parser.parse_pdf('dummy_path_to_pdf_file.pdf')
        self.assertIn('end of the year', parsed_data['Due Date'])

    @patch('src.pdf_parser.extract_text')
    def test_max_funding_non_standard_structure(self, mock_extract_text):
        mock_extract_text.return_value = "Award: $3,000; Grant: $2,500; Scholarship: $4,000."
        parser = PDFParser()
        parsed_data = parser.parse_pdf('dummy_path_to_pdf_file.pdf')
        self.assertIn('$3,000', parsed_data['Max Funding'])

    @patch('src.pdf_parser.extract_text')
    def test_due_date_non_english(self, mock_extract_text):
        mock_extract_text.return_value = "La fecha límite para aplicar es el 31 de diciembre de 2024."
        parser = PDFParser()
        parsed_data = parser.parse_pdf('dummy_path_to_pdf_file.pdf')
        self.assertIn('31 de diciembre de 2024', parsed_data['Due Date'])

    @patch('src.pdf_parser.extract_text')
    def test_max_funding_missing(self, mock_extract_text):
        mock_extract_text.return_value = "The grant will cover various expenses."
        parser = PDFParser()
        parsed_data = parser.parse_pdf('dummy_path_to_pdf_file.pdf')
        self.assertEqual('Not found', parsed_data['Max Funding'])

    @patch('src.pdf_parser.extract_text')
    def test_due_date_missing(self, mock_extract_text):
        mock_extract_text.return_value = "Please submit your application as soon as possible."
        parser = PDFParser()
        parsed_data = parser.parse_pdf('dummy_path_to_pdf_file.pdf')
        self.assertEqual('Not found', parsed_data['Due Date'])

if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    unittest.main()
