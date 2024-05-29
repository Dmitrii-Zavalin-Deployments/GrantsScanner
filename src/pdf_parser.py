from pdfminer.high_level import extract_text

class PDFParser:
    def parse_pdf(self, filepath):
        # Extract text from PDF file
        text = extract_text(filepath)

        # Search for keywords in the text
        data = {
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
        return data

    def search_keyword(self, text, keywords):
        # Search for each keyword in the text and return the sentence containing it
        for keyword in keywords:
            if keyword in text.lower():
                # Find the sentence containing the keyword
                sentences = text.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        return sentence.strip()
        return 'Not found'
