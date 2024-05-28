class QueryBuilder:
    def __init__(self):
        # Load search terms from files
        self.all_words = self.load_search_terms('data/all_words.txt')
        self.all_words = self.load_search_terms('data/any_words.txt')
        self.all_words = self.load_search_terms('data/domains.txt')
        self.all_words = self.load_search_terms('data/none_words.txt')
        

    def build_query(self):
        # Construct the search query
        # ...
        return #query

    @staticmethod
    def load_search_terms(file_path):
        # Load terms from a file
        # ...
        return #terms
