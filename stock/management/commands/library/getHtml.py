import os
import requests as rq

class getHtml():
    def __init__(self, url):
        self.url = url
        self.html_data = rq.get(self.url)
        self.html_data.encoding = self.html_data.apparent_encoding
        self.html_path = None

    def html2output(self):
        return self.html_data.text
    
    def html2file(self, file_path):
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, mode='w') as f:
            f.write(self.html_data.text)

        self.html_path = file_path
        return self.html_path
