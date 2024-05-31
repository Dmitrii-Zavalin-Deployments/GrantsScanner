import unittest
from unittest.mock import patch
from src.file_deleter import FileDeleter

class TestFileDeleter(unittest.TestCase):

    @patch('os.remove')
    def test_delete_existing_file(self, mock_remove):
        # Test deleting an existing file
        file_deleter = FileDeleter('downloaded_file.pdf')
        file_deleter.delete_file()
        mock_remove.assert_called_with('downloaded_file.pdf')

    @patch('os.remove', side_effect=FileNotFoundError)
    def test_delete_non_existing_file(self, mock_remove):
        # Test deleting a non-existing file
        file_deleter = FileDeleter('downloaded_file.pdf')
        file_deleter.delete_file()
        mock_remove.assert_called_with('downloaded_file.pdf')

    @patch('os.remove', side_effect=PermissionError)
    def test_delete_file_permission_error(self, mock_remove):
        # Test deleting a file with a permission error
        file_deleter = FileDeleter('downloaded_file.pdf')
        file_deleter.delete_file()
        mock_remove.assert_called_with('downloaded_file.pdf')

    @patch('os.remove', side_effect=Exception)
    def test_delete_file_generic_exception(self, mock_remove):
        # Test deleting a file with a generic exception
        file_deleter = FileDeleter('downloaded_file.pdf')
        file_deleter.delete_file()
        mock_remove.assert_called_with('downloaded_file.pdf')

if __name__ == '__main__':
    unittest.main()



