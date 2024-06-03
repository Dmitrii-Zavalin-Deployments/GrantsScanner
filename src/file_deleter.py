import os

class FileDeleter:
    def __init__(self, file_path):
        self.file_path = file_path

    def delete_file(self):
        try:
            os.remove(self.file_path)
            print(f"File {self.file_path} has been deleted successfully.")
        except FileNotFoundError:
            print(f"File {self.file_path} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")



