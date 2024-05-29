from src.query_builder import QueryBuilder
from src.search_executor import SearchExecutor
from src.html_generator import HTMLGenerator
from src.pdf_downloader import PDFDownloader
# ... other imports

def main():
    # Initialize modules
    # query_builder = QueryBuilder()
    # search_executor = SearchExecutor()
    html_generator = HTMLGenerator('data/grants.json')
    downloader = PDFDownloader()
    # ... other module initializations

    # Build the search query
    # query = query_builder.build_query()
    
    # Execute the search and get PDF links
    pdf_links = [] # search_executor.execute_search(query)
    
    # Continue with downloading, parsing, aggregating
    for pdf_url in pdf_links:
        downloader.download_pdf(pdf_url)
    # 
    # Generating HTML 
    html_generator.generate_html()

if __name__ == "__main__":
    main()
