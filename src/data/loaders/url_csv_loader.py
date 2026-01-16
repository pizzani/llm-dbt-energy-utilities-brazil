from src.data.loaders.base_loader import *
import requests
import csv
from io import StringIO

class URLCSVLoader(BaseLoader):
    def __init__(self, url: str, sep=";"):
        self.url = url
        self.sep = sep
        self._data = None

    def load(self):
        response = requests.get(self.url)
        response.raise_for_status()
        
        csv_file = StringIO(response.text)
        reader = csv.DictReader(csv_file, delimiter=self.sep)
        self._data = list(reader)
        return self._data

    def get_headers(self):
        if not self._data:
            return []
        return list(self._data[0].keys())