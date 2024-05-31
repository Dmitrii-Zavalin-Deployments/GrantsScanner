import unittest
from unittest.mock import patch, mock_open
from src.query_builder import QueryBuilder

class TestQueryBuilder(unittest.TestCase):

    @patch('os.getenv')
    @patch('builtins.open', new_callable=mock_open, read_data='word1\nword2\nword3')
    def test_load_search_terms(self, mock_file, mock_env):
        # Test loading search terms from a file
        mock_env.return_value = '1'
        qb = QueryBuilder()
        self.assertEqual(qb.load_search_terms('data/all_words.txt'), ['word1', 'word2', 'word3'])

    @patch('os.getenv')
    @patch('builtins.open', new_callable=mock_open, read_data='{"0": {"name": "domain1", "query": "query1"}}')
    @patch('json.load')
    def test_load_domains(self, mock_json_load):
        # Mocking json.load to return the expected domains list
        mock_json_load.return_value = [{'name': 'domain1', 'query': 'query1'}]
        qb = QueryBuilder()
        self.assertEqual(qb.load_domains(), {'0': {'name': 'domain1', 'query': 'query1'}})

    @patch('os.getenv')
    def test_get_next_domain_key(self, mock_env):
        # Test getting the next domain key
        mock_env.return_value = '1'
        qb = QueryBuilder()
        with patch('query_builder.QueryBuilder.load_domains', return_value={'0': {}, '1': {}, '2': {}}):
            self.assertEqual(qb.get_next_domain_key(), 3)

    @patch('os.getenv')
    def test_current_number_of_domain(self, mock_env):
        # Test current number of domain calculation
        mock_env.return_value = '5'
        qb = QueryBuilder()
        with patch('query_builder.QueryBuilder.get_next_domain_key', return_value=3):
            self.assertEqual(qb.current_number_of_domain(), 2)

    @patch('os.getenv')
    def test_get_query_data(self, mock_env):
        # Test getting query data
        mock_env.return_value = '1'
        qb = QueryBuilder()
        with patch('query_builder.QueryBuilder.load_domains', return_value={'1': {'name': 'domain2', 'query': 'query2'}}):
            self.assertEqual(qb.get_query_data(), {'name': 'domain2', 'query': 'query'})

    @patch('os.getenv')
    def test_build_query(self, mock_env):
        # Test building a query
        mock_env.return_value = '1'
        qb = QueryBuilder()
        self.assertEqual(qb.build_query(), 'query')

if __name__ == '__main__':
    unittest.main()



