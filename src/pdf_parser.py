from deep_translator import GoogleTranslator
from datetime import datetime
from pdfminer.high_level import extract_text
import re

class PDFParser:
    def __init__(self):
        self.current_year = datetime.now().year
        self.funding_pattern = re.compile(
            r'(?:රු\ or\ ரூ|ج\.س\.|ج\.م\.|ر\.ي\.|ر\.ع\.|د\.م\.|د\.ج\.|د\.ب\.|Ptas\.|د\.ع\.|ف\.ج\.|ل\.س\.|ر\.ق\.|ل\.ل\.|د\.ت\.|د\.إ\.|ر\.س\.|ل\.د\.|د\.ك\.|أ\.م\.|د\.أ\.|Bs\.F|ناكفا|руб\.|MOP\$|դր\.|B\.|Fr\.|Bs\.|Nu\.|лв\.|S\.|kr\.|C\$|сум|SS£|р\.|TSh|дин|FBu|ден|Ssh|грн|R\$|\.ރ|KSh|CF|КМ|Sh|Sl|Ar|kr|Le|Db|SM|\$|zł|PT|դր|Ks|¥元|MK|RM|Kč|VT|ST|FG|kn|Kz|रु|ZK|रू|Rs|MT|Ft|R₣|ብር|Rp|₮|៛|€|₱|₣|₵|₼|฿|£|₽|₫|৳|圓|D|ƒ|₦|₲|₹|﷼|G|₩|؋|L|₭|R|с|K|P|T|¥|₺|₪|₸|₾|₡)\s?\d+|\d+\s?(?:රු\ or\ ரூ|ج\.س\.|ج\.م\.|ر\.ي\.|ر\.ع\.|د\.م\.|د\.ج\.|د\.ب\.|Ptas\.|د\.ع\.|ف\.ج\.|ل\.س\.|ر\.ق\.|ل\.ل\.|د\.ت\.|د\.إ\.|ر\.س\.|ل\.د\.|د\.ك\.|أ\.م\.|د\.أ\.|Bs\.F|ناكفا|руб\.|MOP\$|դր\.|B\.|Fr\.|Bs\.|Nu\.|лв\.|S\.|kr\.|C\$|сум|SS£|р\.|TSh|дин|FBu|ден|Ssh|грн|R\$|\.ރ|KSh|CF|КМ|Sh|Sl|Ar|kr|Le|Db|SM|\$|zł|PT|դր|Ks|¥元|MK|RM|Kč|VT|ST|FG|kn|Kz|रु|ZK|रू|Rs|MT|Ft|R₣|ብር|Rp|₮|៛|€|₱|₣|₵|₼|฿|£|₽|₫|৳|圓|D|ƒ|₦|₲|₹|﷼|G|₩|؋|L|₭|R|с|K|P|T|¥|₺|₪|₸|₾|₡)'
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
                'fund', 'financial support', 'budget', 'voucher', 
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
                return sentence

        return 'Not found'

