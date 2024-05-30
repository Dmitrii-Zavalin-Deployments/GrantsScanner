from deep_translator import GoogleTranslator
from datetime import datetime
from pdfminer.high_level import extract_text
import re

class PDFParser:
    def __init__(self):
        self.current_year = datetime.now().year
        self.next_year = self.current_year + 1
        self.funding_pattern = re.compile(
            r'(?<![^ \t\n.,!?:;"\')\]}])(?:රු\ or\ ரூ|ج\.س\.|ج\.م\.|ر\.ي\.|ر\.ع\.|د\.م\.|د\.ج\.|د\.ب\.|Ptas\.|د\.ع\.|ف\.ج\.|ل\.س\.|ر\.ق\.|ل\.ل\.|د\.ت\.|د\.إ\.|ر\.س\.|ل\.د\.|د\.ك\.|أ\.م\.|د\.أ\.|Bs\.F|ناكفا|руб\.|MOP\$|դր\.|B\.|Fr\.|Bs\.|Nu\.|лв\.|S\.|kr\.|C\$|сум|SS£|р\.|TSh|дин|FBu|ден|Ssh|грн|R\$|\.ރ|KSh|CF|КМ|Sh|Sl|Ar|kr|Le|Db|SM|\$|zł|PT|դր|Ks|¥元|MK|RM|Kč|VT|ST|FG|kn|Kz|रु|ZK|रू|Rs|MT|Ft|R₣|ብር|Rp|₮|៛|€|₱|₣|₵|₼|฿|£|₽|₫|৳|圓|D|ƒ|₦|₲|₹|﷼|G|₩|؋|L|₭|R|с|K|P|T|¥|₺|₪|₸|₾|₡)\s*\d+(?:,\d{3})*(?:\.\d+)?|(?:\d+(?:,\d{3})*(?:\.\d+)?\s*(?:රු\ or\ ரூ|ج\.س\.|ج\.م\.|ر\.ي\.|ر\.ع\.|د\.م\.|د\.ج\.|د\.ب\.|Ptas\.|د\.ع\.|ف\.ج\.|ل\.س\.|ر\.ق\.|ل\.ل\.|د\.ت\.|د\.إ\.|ر\.س\.|ل\.د\.|د\.ك\.|أ\.م\.|د\.أ\.|Bs\.F|ناكفا|руб\.|MOP\$|դր\.|B\.|Fr\.|Bs\.|Nu\.|лв\.|S\.|kr\.|C\$|сум|SS£|р\.|TSh|дин|FBu|ден|Ssh|грн|R\$|\.ރ|KSh|CF|КМ|Sh|Sl|Ar|kr|Le|Db|SM|\$|zł|PT|դր|Ks|¥元|MK|RM|Kč|VT|ST|FG|kn|Kz|रु|ZK|रू|Rs|MT|Ft|R₣|ብር|Rp|₮|៛|€|₱|₣|₵|₼|฿|£|₽|₫|৳|圓|D|ƒ|₦|₲|₹|﷼|G|₩|؋|L|₭|R|с|K|P|T|¥|₺|₪|₸|₾|₡)(?![^\s.,!?:;"\')\]}]))'
        )
        self.date_pattern_short = re.compile(
            rf'(?:0?[1-9]|1[012])/(?:0?[1-9]|[12][0-9]|3[01])/({self.current_year}|{self.next_year})',
        )

    def parse_pdf(self, filepath):
        text_in_english = ''
        funds = []
        dates = []
        requirements = []
        documents = []
        summary =[]

        try:
            text = extract_text(filepath).replace('\n', ' ')
            chunks = [text[i:i+4500] for i in range(0, len(text), 4500)]
            translator = GoogleTranslator(source='auto', target='en')
            for chunk in chunks:
                text_in_english += translator.translate(chunk)
        except Exception as e:
            print(f"Error: The file was not recognized as a pdf file. {e}")
            return {'Funds': funds, 'Dates': dates, 'Requirements': requirements, 'Documents': documents, 'Summary': summary}

        sentences = re.split(r'(?<=[.!?])\s+|\n', text_in_english)
        
        for sentence in sentences:
            if self.funding_pattern.search(sentence):
                funds.append(sentence)
            if self.date_pattern_short.search(sentence):
                dates.append(sentence)
            if self.search_keyword(sentence, [
                'Jan', 'January', 'Feb', 'February',
                'Mar', 'March', 'Apr', 'April', 'May',
                'Jun', 'June', 'Jul', 'July', 'Aug',
                'August', 'Sep', 'September', 'Oct', 'October',
                'Nov', 'November', 'Dec', 'December'
            ]):
                if self.search_keyword(sentence, [
                    str(self.current_year), str(self.next_year)
                ]):
                    dates.append(sentence)
                    
            if self.search_keyword(sentence, [
                'requirement', 'eligibility', 'criteria', 'qualification'
            ]):
                requirements.append(sentence)
            if self.search_keyword(sentence, [
                'document', 'submission',
                'proposal',
                'application form', 'checklist'
            ]):
                documents.append(sentence)

        summary = self.create_summary(sentences, funds, dates, requirements, documents)
        
        data = {
            'Funds': funds,
            'Dates': dates,
            'Requirements': requirements,
            'Documents': documents,
            'Summary': summary
        }

        return data

    def search_keyword(self, text, keywords):
        for keyword in keywords:
            if keyword.upper() in text.upper():
                return True
            
            keyword_plural = (keyword[:-1] + "ies") if keyword.endswith("y") else (keyword + "s")
            #print(keyword)
            #print(keyword_plural)
            
            if keyword_plural.upper() in text.upper():
                return True

        return False
    
    def create_summary(self, sentences, funds, dates, requirements, documents):
        summary = []
        for sentence in sentences:
            if sentence in funds or sentence in dates or sentence in requirements or sentence in documents:
                summary.append(sentence)
        
        return summary
    