import os
import json

class QueryBuilder:
    def __init__(self):
        # Load search terms from files
        self.all_words = self.load_search_terms('data/all_words.txt')
        self.any_words = self.load_search_terms('data/any_words.txt')
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

    def load_domains(self):
        # Read the domains.json file and create a dictionary with incremental keys starting from 0
        with open('data/domains.json', 'r') as file:
            domains_list = json.load(file)
        
        domains_dict = {str(i): domain for i, domain in enumerate(domains_list)}
        return domains_dict

    def get_next_domain_key(self):
            domains_dict = self.load_domains()
            max_key = max(map(int, domains_dict.keys()))  # Convert keys to integers and find the max
            return max_key + 1
    
    def current_number_of_domain(self):
        next_domain_key = self.get_next_domain_key()
        if self.run_number is not None:
            return int(self.run_number) % next_domain_key
        else:
            return 0  # Default to 0 if run_number is not set
    