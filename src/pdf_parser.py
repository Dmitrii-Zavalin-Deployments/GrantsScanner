import re
from datetime import datetime
from pdfminer.high_level import extract_text

class PDFParser:
    def __init__(self):
        current_year = datetime.now().year
        # Patterns for matching funding amounts and dates
        self.funding_pattern = re.compile(r'(\$\d+(?:,\d{3})*(?:\.\d+)?)|(?:\b\d+(?:,\d{3})*\b)')
        self.date_pattern = re.compile(rf'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+(?:{current_year}|{current_year + 1})\b')

    def parse_pdf(self, filepath):
        # Extract text from PDF file
        text = extract_text(filepath).replace('\n', ' ')

        # First, search for keywords in the text
        keyword_data = {
            'Max Funding': self.search_keyword(text, [
                'maximum funding', 'max funding', 'funding amount',
                'funds requested', 'financial support', 'budget',
                'amount of grant', 'total funding', 'grant size'
            ]),
            'Due Date': self.search_keyword(text, [
                'application deadline', 'submission deadline', 'due date',
                'letters of intent', 'proposal submission', 'application period',
                'closing date', 'deadline for submission', 'proposal due date'
            ]),
            'Requirements': self.search_keyword(text, [
                'applicant requirements', 'eligibility criteria',
                'principal investigator', 'research team', 'qualification criteria',
                'eligibility requirements', 'applicant qualifications'
            ]),
            'Submission Items': self.search_keyword(text, [
                'required documents', 'submission items', 'application items',
                'proposal content', 'application form', 'supporting documents',
                'proposal submission details', 'documents to be submitted',
                'application components', 'submission checklist'
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
        # Search for each keyword or phrase in the text using regex to allow for intervening words
        for keyword in keywords:
            # Create a regex pattern that allows for other words between the keywords
            pattern = r'\b' + r'.*?'.join(keyword.split()) + r'.*?\b'
            regex = re.compile(pattern, re.IGNORECASE)
            match = regex.search(text)
            if match:
                # Return the matched text without newline characters and extra spaces
                return ' '.join(match.group(0).split())
        return 'Not found'

    def match_regex(self, text, pattern):
        # Apply regex pattern to text
        match = pattern.search(text)
        if match:
            # Return the matched text without newline characters and extra spaces
            return ' '.join(match.group(0).split())
        return 'Not found'

