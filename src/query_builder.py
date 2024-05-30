import os

class QueryBuilder:
    def __init__(self):
        # Load search terms from files
        self.all_words = self.load_search_terms('data/all_words.txt')
        self.any_words = self.load_search_terms('data/any_words.txt')
        self.domains = self.load_search_terms('data/domains.txt')
        self.none_words = self.load_search_terms('data/none_words.txt')
        self.run_number = os.getenv('GITHUB_RUN_NUMBER')

    def build_query(self):
        # Construct the search query using the run number
        # ...
        return "query"

    def get_query_data(self):
        # Generate the dictionary with "name" and "query"
        return {
            "name": "name_data",
            "query": self.build_query()
        }

    @staticmethod
    def load_search_terms(file_path):
        # Load terms from a file
        # ...
        return #terms
    
    
    