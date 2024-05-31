import json
import os
import logging

class DataAggregator:
    def __init__(self, grants_file_path):
        self.grants_file_path = grants_file_path
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def read_grants_data(self):
        if os.path.exists(self.grants_file_path) and os.path.getsize(self.grants_file_path) > 0:
            with open(self.grants_file_path, 'r') as file:
                return json.load(file)
        else:
            return {}

    def write_grants_data(self, data):
        with open(self.grants_file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def add_grant_data(self, query_data, pdf_url, parsed_data):
        grants_data = self.read_grants_data()
        
        # Check if the PDF URL already exists in the system
        for grant_id, grant_info in grants_data.items():
            if grant_info.get('link') == pdf_url:
                print(f"The grant with url: {pdf_url} is already in the system.")
                return
        
        # If the PDF URL does not exist, create a new entry
        new_grant_data = {
            "name": query_data["name"],
            "funds": parsed_data["Funds"],
            "dates": parsed_data["Dates"],
            "requirements": parsed_data["Requirements"],
            "documents": parsed_data["Documents"],
            "summary": parsed_data["Summary"],
            "link": pdf_url,
            "query": query_data["query"]
        }
        
        # Find the next available key
        next_key = str(max([int(k) for k in grants_data.keys()], default=-1) + 1)
        grants_data[next_key] = new_grant_data
        
        # Write the updated data back to the file
        self.write_grants_data(grants_data)
        print(f"Added new grant data for url: {pdf_url}")




