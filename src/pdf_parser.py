from deep_translator import GoogleTranslator
from datetime import datetime
from pdfminer.high_level import extract_text
import re

class PDFParser:
    def __init__(self):
        self.current_year = datetime.now().year
        self.funding_pattern = re.compile(
            r'(\$\d{1,3}(?:,\d{3})*(?:\.\d+)?(?:\s?(?:million|billion|thousand))?|\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b(?:\s?[A-Za-z]{3})?)'
        )
        self.date_pattern = re.compile(
           rf'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(?:\d{{1,2}}(?:st|nd|rd|th)?|(?<=\b)\d{{1,2}}(?:st|nd|rd|th)?\b),?\s+{self.current_year}\b|\b{self.current_year}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{{1,2}}(?:st|nd|rd|th)?\b|\b\d{{1,2}}(?:st|nd|rd|th)?\s+of\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?),?\s+\d{{4}}\b'
        )

    def parse_pdf(self, filepath):
        text_in_english = ''
        try:
            text = extract_text(filepath).replace('\n', ' ')
            # Split the text into chunks of 4500 characters
            chunks = [text[i:i+4500] for i in range(0, len(text), 4500)]
            translator = GoogleTranslator(source='auto', target='en')
            # Translate each chunk and concatenate
            for chunk in chunks:
                text_in_english += translator.translate(chunk)
        except Exception as e:
            print(f"Error: The file was not recognized as a pdf file. {e}")
            return {'Max Funding': 'Not found', 'Due Date': 'Not found', 'Requirements': 'Not found', 'Submission Items': 'Not found'}

        # print(text_in_english)
        
        keyword_data = {
            'Max Funding': self.search_keyword(text_in_english, [
                'fund', 'financial support', 'budget',
                'funding', 'request', 'requested', 'grant'
            ]),
            'Due Date': self.search_keyword(text_in_english, [
                'application deadline', 'submission deadline', 'due date',
                'letter of intent', 'proposal submission', 'application period',
                'closing date', 'deadline for submission', 'proposal due date',
                'submission', 'application', 'deadline'
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
        
        print(keyword_data['Max Funding'])

        data = {
            'Max Funding': self.match_regex(keyword_data['Max Funding'], self.funding_pattern),
            'Due Date': self.match_regex(keyword_data['Due Date'], self.date_pattern),
            'Requirements': keyword_data['Requirements'],  # No regex needed
            'Submission Items': keyword_data['Submission Items']  # No regex needed
        }

        return data

    def search_keyword(self, text, keywords):
        for keyword in keywords:
            # Create a pattern that matches both singular and plural forms
            pattern_parts = []
            for word in keyword.split():
                if word.endswith('s'):
                    pattern_parts.append(r'\b' + re.escape(word[:-1]) + r's?\b')
                else:
                    pattern_parts.append(r'\b' + re.escape(word) + r's?\b')
            pattern = r'([^.!?]*' + r'.*?'.join(pattern_parts) + r'.*?[.!?])'
            regex = re.compile(pattern, re.IGNORECASE)
            matches = regex.findall(text)
            if matches:
                # Return the longest match to ensure full context
                return max(matches, key=len).strip()
        return 'Not found'

    def match_regex(self, text, pattern):
        sentences = re.split(r'(?<=[.!?]) +', text)
        for sentence in sentences:
            matches = pattern.findall(sentence)
            if matches:
                # If there are multiple monetary values, return the entire sentence
                # if len(matches) > 1:
                return sentence
                # If there's only one monetary value, return just that value
                # return ' '.join(matches)
        return 'Not found'

