from unittest.mock import patch, Mock
from src.data.loaders.url_json_loader import URLJSONLoader

@patch("requests.get")
def test_url_json_loader(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = [{"id": 1, "name": "Alice"}]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    loader = URLJSONLoader("http://fakeurl.com/data.json")
    data = loader.load()

    assert isinstance(data, list)
    assert data == [{"id": 1, "name": "Alice"}]
    assert loader.get_headers() == ["id", "name"]