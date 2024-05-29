import re
from pdfminer.high_level import extract_text

class PDFParser:
    def __init__(self):
        # Patterns for matching funding amounts and dates
        self.funding_pattern = re.compile(r'(\$\d+(?:,\d{3})*(?:\.\d+)?)|(?:\b\d+(?:,\d{3})*\b)')
        self.date_pattern = re.compile(r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}\b')

    def parse_pdf(self, filepath):
        # Extract text from PDF file
        text = extract_text(filepath)

        # First, search for keywords in the text
        keyword_data = {
            'Max Funding': self.search_keyword(text, [
                'maximum funding', 'max funding', 'funding amount',
                'funds requested', 'financial support', 'budget'
            ]),
            'Due Date': self.search_keyword(text, [
                'application deadline', 'submission deadline', 'due date',
                'letters of intent', 'proposal submission', 'application period'
            ]),
            'Requirements': self.search_keyword(text, [
                'applicant requirements', 'eligibility criteria',
                'principal investigator', 'research team', 'qualification criteria'
            ]),
            'Submission Items': self.search_keyword(text, [
                'required documents', 'submission items', 'application items',
                'proposal content', 'application form', 'supporting documents'
            ])
        }

        # Then, apply regex patterns where needed
        data = {
            'Max Funding': self.match_regex(keyword_data['Max Funding'], self.funding_pattern),
            'Due Date': self.match_regex(keyword_data['Due Date'], self.date_pattern),
            'Requirements': keyword_data['Requirements'],  # No regex needed
            'Submission Items': keyword_data['Submission Items']  # No regex needed
        }

        return data

    def search_keyword(self, text, keywords):
        # Search for each keyword in the text and return the sentence containing it
        for keyword in keywords:
            if keyword in text.lower():
                sentences = text.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        return sentence.strip()
        return 'Not found'

    def match_regex(self, text, pattern):
        # Apply regex pattern to text
        if text != 'Not found':
            match = pattern.search(text)
            if match:
                return match.group()
        return 'Not found'
