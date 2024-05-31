from src.query_builder import QueryBuilder
from src.search_executor import SearchExecutor
from src.html_generator import HTMLGenerator
from src.pdf_downloader import PDFDownloader
from src.pdf_parser import PDFParser
from src.data_aggregator import DataAggregator
from src.file_deleter import FileDeleter

def main():
    # Initialize modules
    query_builder = QueryBuilder()
    # search_executor = SearchExecutor()
    downloader = PDFDownloader()
    parser = PDFParser()
    aggregator = DataAggregator('data/grants.json')
    deleter = FileDeleter('downloaded_file.pdf')
    html_generator = HTMLGenerator()
    
    # ... other module initializations

    # Build the search query
    query_data = query_builder.get_query_data()
    # print(f'Domain: {query_data["name"]}')
    # print(f'Query: {query_data["query"]}')
    
    # Execute the search and get PDF links
    pdf_links = ["https://www.eggfarmers.ca/wp-content/uploads/2024/01/2024-Call-for-LOIs_Applicant-Information-Package_ENG.pdf"] # search_executor.execute_search(query)
    
    # Continue with downloading, parsing, aggregating
    for pdf_url in pdf_links:
        # Download pdf from each link
        # downloader.download_pdf(pdf_url) # Commented not to spam on testing
        # Parse pdf from each download
        parsed_data = parser.parse_pdf('downloaded_file.pdf')
        print('Data is parsed')
        # print(parsed_data)
        # Delete parsed pdf file
        deleter.delete_file()
        # Aggregate data for grants.json and html
        grants_data = aggregator.add_grant_data(query_data, pdf_url, parsed_data)
        # Generating HTML 
        html_generator.generate_html(grants_data)

if __name__ == "__main__":
    main()
