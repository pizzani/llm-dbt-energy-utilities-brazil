from src.data.loaders.base_loader import *
import requests

class URLJSONLoader(BaseLoader):
    def __init__(self, url: str):
      self.url = url
      
    def load(self):
        response = requests.get(self.url)
        response.raise_for_status()
        self._data = response.json()
        return self._data

    def get_headers(self):
        if not self._data:
            return []
        return list(self._data[0].keys())