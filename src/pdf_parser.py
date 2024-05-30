from deep_translator import GoogleTranslator
from datetime import datetime
from pdfminer.high_level import extract_text
import re

class PDFParser:
    def __init__(self):
        self.current_year = datetime.now().year
        self.funding_pattern = re.compile(
            r'(?<![^ \t\n.,!?:;"\')\]}])(?:රු\ or\ ரூ|ج\.س\.|ج\.م\.|ر\.ي\.|ر\.ع\.|د\.م\.|د\.ج\.|د\.ب\.|Ptas\.|د\.ع\.|ف\.ج\.|ل\.س\.|ر\.ق\.|ل\.ل\.|د\.ت\.|د\.إ\.|ر\.س\.|ل\.د\.|د\.ك\.|أ\.م\.|د\.أ\.|Bs\.F|ناكفا|руб\.|MOP\$|դր\.|B\.|Fr\.|Bs\.|Nu\.|лв\.|S\.|kr\.|C\$|сум|SS£|р\.|TSh|дин|FBu|ден|Ssh|грн|R\$|\.ރ|KSh|CF|КМ|Sh|Sl|Ar|kr|Le|Db|SM|\$|zł|PT|դր|Ks|¥元|MK|RM|Kč|VT|ST|FG|kn|Kz|रु|ZK|रू|Rs|MT|Ft|R₣|ብር|Rp|₮|៛|€|₱|₣|₵|₼|฿|£|₽|₫|৳|圓|D|ƒ|₦|₲|₹|﷼|G|₩|؋|L|₭|R|с|K|P|T|¥|₺|₪|₸|₾|₡)\s*\d+(?:,\d{3})*(?:\.\d+)?|(?:\d+(?:,\d{3})*(?:\.\d+)?\s*(?:රු\ or\ ரூ|ج\.س\.|ج\.م\.|ر\.ي\.|ر\.ع\.|د\.م\.|د\.ج\.|د\.ب\.|Ptas\.|د\.ع\.|ف\.ج\.|ل\.س\.|ر\.ق\.|ل\.ل\.|د\.ت\.|د\.إ\.|ر\.س\.|ل\.د\.|د\.ك\.|أ\.م\.|د\.أ\.|Bs\.F|ناكفا|руб\.|MOP\$|դր\.|B\.|Fr\.|Bs\.|Nu\.|лв\.|S\.|kr\.|C\$|сум|SS£|р\.|TSh|дин|FBu|ден|Ssh|грн|R\$|\.ރ|KSh|CF|КМ|Sh|Sl|Ar|kr|Le|Db|SM|\$|zł|PT|դր|Ks|¥元|MK|RM|Kč|VT|ST|FG|kn|Kz|रु|ZK|रू|Rs|MT|Ft|R₣|ብር|Rp|₮|៛|€|₱|₣|₵|₼|฿|£|₽|₫|৳|圓|D|ƒ|₦|₲|₹|﷼|G|₩|؋|L|₭|R|с|K|P|T|¥|₺|₪|₸|₾|₡)(?![^\s.,!?:;"\')\]}]))'
        )
        self.date_pattern = re.compile(
           rf'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(?:\d{{1,2}}(?:st|nd|rd|th)?|(?<=\b)\d{{1,2}}(?:st|nd|rd|th)?\b),?\s+{self.current_year}\b|\b{self.current_year}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{{1,2}}(?:st|nd|rd|th)?\b|\b\d{{1,2}}(?:st|nd|rd|th)?\s+of\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?),?\s+\d{{4}}\b'
        )

    def parse_pdf(self, filepath):
        text_in_english = ''
        prices = []
        dates = []
        requirements = []
        documents = []

        try:
            text = extract_text(filepath).replace('\n', ' ')
            chunks = [text[i:i+4500] for i in range(0, len(text), 4500)]
            translator = GoogleTranslator(source='auto', target='en')
            for chunk in chunks:
                text_in_english += translator.translate(chunk)
        except Exception as e:
            print(f"Error: The file was not recognized as a pdf file. {e}")
            return {'Prices': prices, 'Dates': dates, 'Requirements': requirements, 'Documents': documents}

        sentences = re.split(r'(?<=[.!?]) +', text_in_english)
        for sentence in sentences:
            if self.funding_pattern.search(sentence):
                prices.append(sentence)
            if self.date_pattern.search(sentence):
                dates.append(sentence)
            if self.search_keyword(sentence, [
                'applicant requirements', 'eligibility criteria',
                'principal investigator', 'research team', 'qualification criteria',
                'eligibility requirements', 'applicant qualifications'
            ]):
                requirements.append(sentence)
            if self.search_keyword(sentence, [
                'required documents', 'submission items', 'application items',
                'proposal content', 'application form', 'supporting documents',
                'proposal submission details', 'documents to be submitted',
                'application components', 'submission checklist'
            ]):
                documents.append(sentence)

        data = {
            'Prices': prices,
            'Dates': dates,
            'Requirements': requirements,
            'Documents': documents
        }

        return data

    def search_keyword(self, text, keywords):
        for keyword in keywords:
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
                return max(matches, key=len).strip()
        return 'Not found'

    def match_regex(self, text, pattern):
        sentences = re.split(r'(?<=[.!?])\s+|\n', text)
        for sentence in sentences:
            matches = pattern.findall(sentence)
            if matches:
                return sentence
        return 'Not found'
    
    
    