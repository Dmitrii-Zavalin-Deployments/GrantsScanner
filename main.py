from src.query_builder import QueryBuilder
from src.search_executor import SearchExecutor
from src.html_generator import HTMLGenerator
from src.pdf_downloader import PDFDownloader
from src.pdf_parser import PDFParser
# ... other imports

def main():
    # Initialize modules
    query_builder = QueryBuilder()
    # search_executor = SearchExecutor()
    html_generator = HTMLGenerator('data/grants.json')
    downloader = PDFDownloader()
    parser = PDFParser()
    
    # ... other module initializations

    # Build the search query
    query_data = query_builder.get_query_data()
    print(f'Domain: {query_data["name"]}')
    print(f'Query: {query_data["query"]}')
    
    # Execute the search and get PDF links
    pdf_links = ["https://www.eggfarmers.ca/wp-content/uploads/2024/01/2024-Call-for-LOIs_Applicant-Information-Package_ENG.pdf"] # search_executor.execute_search(query)
    
    # Continue with downloading, parsing, aggregating
    for pdf_url in pdf_links:
        # Download pdf from each link
        # downloader.download_pdf(pdf_url) # Commented for not spamming on tests
        # Parse pdf from each download
        # parsed_data = parser.parse_pdf('downloaded_file.pdf')
        print('Parsed data: ')
        # print(parsed_data)
    # 
    # Generating HTML 
    html_generator.generate_html()

if __name__ == "__main__":
    main()
