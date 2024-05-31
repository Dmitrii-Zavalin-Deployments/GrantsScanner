import unittest
from unittest.mock import patch, MagicMock
from src.pdf_parser import PDFParser
from datetime import datetime

class TestPDFParser(unittest.TestCase):

    def setUp(self):
        self.parser = PDFParser()

    def test_initialization(self):
        self.assertEqual(self.parser.current_year, datetime.now().year)

    @patch('src.pdf_parser.extract_text')
    @patch('src.pdf_parser.GoogleTranslator.translate')
    def test_parse_pdf_valid(self, mock_translate, mock_extract_text):
        mock_extract_text.return_value = 'Sample text with funding and date 2021'
        mock_translate.return_value = 'Sample text with funding and date 2021'
        result = self.parser.parse_pdf('path/to/file.pdf')
        self.assertIn('Funds', result)
        self.assertIn('Dates', result)
        self.assertIn('Requirements', result)
        self.assertIn('Documents', result)
        self.assertIn('Summary', result)

    @patch('src.pdf_parser.extract_text', side_effect=Exception('Invalid file'))
    def test_parse_pdf_invalid_file(self, mock_extract_text):
        result = self.parser.parse_pdf('invalid/path')
        self.assertEqual(result, {'Funds': [], 'Dates': [], 'Requirements': [], 'Documents': [], 'Summary': []})

    def test_search_keyword_found(self):
        self.assertTrue(self.parser.search_keyword('We have a requirement', ['requirement']))

    def test_search_keyword_not_found(self):
        self.assertFalse(self.parser.search_keyword('No keyword here', ['requirement']))

    def test_create_summary(self):
        sentences = ['Sentence with funding.', 'Sentence with date.', 'Sentence with requirement.', 'Sentence with document.']
        funds = ['Sentence with funding.']
        dates = ['Sentence with date.']
        requirements = ['Sentence with requirement.']
        documents = ['Sentence with document.']
        summary = self.parser.create_summary(sentences, funds, dates, requirements, documents)
        self.assertEqual(summary, sentences)

    def test_search_keyword_plural_form(self):
        self.assertTrue(self.parser.search_keyword('We have many requirements', ['requirement']))

    @patch('src.pdf_parser.extract_text')
    def test_parse_pdf_no_funds(self, mock_extract_text):
        mock_extract_text.return_value = 'Sample text without funding'
        result = self.parser.parse_pdf('path/to/file.pdf')
        self.assertEqual(result['Funds'], [])

    @patch('src.pdf_parser.extract_text')
    def test_parse_pdf_no_dates(self, mock_extract_text):
        mock_extract_text.return_value = 'Sample text without dates'
        result = self.parser.parse_pdf('path/to/file.pdf')
        self.assertEqual(result['Dates'], [])

    @patch('src.pdf_parser.extract_text')
    def test_parse_pdf_with_mixed_content(self, mock_extract_text):
        mock_extract_text.return_value = 'Funding of $1000 on 1st January 2024. Requirements include application form.'
        result = self.parser.parse_pdf('path/to/mixed-content.pdf')
        self.assertIn('Funding of $1000 on 1st January 2024.', result['Funds'])
        self.assertIn('Funding of $1000 on 1st January 2024.', result['Dates'])
        self.assertIn('Requirements include application form.', result['Requirements'])

    @patch('src.pdf_parser.extract_text')
    def test_parse_pdf_with_complex_currency_patterns(self, mock_extract_text):
        mock_extract_text.return_value = 'Award of ₹10,00,000. Grant of €500,000.'
        result = self.parser.parse_pdf('path/to/complex-currency.pdf')
        self.assertIn('Award of ₹10,00,000.', result['Funds'])
        self.assertIn('Grant of €500,000.', result['Funds'])

    @patch('src.pdf_parser.extract_text')
    def test_parse_pdf_empty_content(self, mock_extract_text):
        mock_extract_text.return_value = ''
        result = self.parser.parse_pdf('path/to/empty.pdf')
        self.assertEqual(result, {'Funds': [], 'Dates': [], 'Requirements': [], 'Documents': [], 'Summary': []})

    @patch('src.pdf_parser.extract_text')
    def test_parse_pdf_with_multiple_date_formats(self, mock_extract_text):
        mock_extract_text.return_value = 'The event will be held on 03/25/2024 and 25th March 2024.'
        result = self.parser.parse_pdf('path/to/multiple-date-formats.pdf')
        self.assertIn('The event will be held on 03/25/2024 and 25th March 2024.', result['Dates'])
        self.assertIn('The event will be held on 03/25/2024 and 25th March 2024.', result['Dates'])

    @patch('src.pdf_parser.extract_text')
    def test_parse_pdf_with_unrecognized_currency(self, mock_extract_text):
        mock_extract_text.return_value = 'A budget of 1000 Galactic Credits was approved.'
        result = self.parser.parse_pdf('path/to/unrecognized-currency.pdf')
        self.assertNotIn('A budget of 1000 Galactic Credits was approved.', result['Funds'])

    @patch('src.pdf_parser.extract_text')
    def test_parse_pdf_with_nested_requirements(self, mock_extract_text):
        mock_extract_text.return_value = 'Requirements: Submit application form, which includes personal statement and references.'
        result = self.parser.parse_pdf('path/to/nested-requirements.pdf')
        self.assertIn('Requirements: Submit application form, which includes personal statement and references.', result['Requirements'])

    @patch('src.pdf_parser.extract_text')
    def test_parse_pdf_with_overlapping_categories(self, mock_extract_text):
        mock_extract_text.return_value = 'Submit by 5th May 2024: Funding application and eligibility criteria.'
        result = self.parser.parse_pdf('path/to/overlapping-categories.pdf')
        self.assertIn('Submit by 5th May 2024: Funding application and eligibility criteria.', result['Summary'])

if __name__ == '__main__':
    unittest.main()

