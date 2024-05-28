from src.query_builder import QueryBuilder
from src.search_executor import SearchExecutor
from src.html_generator import HTMLGenerator
# ... other imports

def main():
    # Initialize modules
    # query_builder = QueryBuilder()
    # search_executor = SearchExecutor()
    html_generator = HTMLGenerator('/data/grants.json')
    # ... other module initializations

    # Build the search query
    # query = query_builder.build_query()
    
    # Execute the search and get PDF links
    # pdf_links = search_executor.execute_search(query)
    
    # ... continue with downloading, parsing, aggregating,
    # 
    # Generating HTML 
    html_generator.generate_html()

if __name__ == "__main__":
    main()
