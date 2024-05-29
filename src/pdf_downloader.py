import os
import requests

class PDFDownloader:
    def download_pdf(self, url, filename='downloaded_file.pdf'):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"File saved as {filename}")
                return filename
            else:
                print(f"Failed to download the file. Status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"A request error occurred: {e}")
            return None
