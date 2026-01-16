from unittest.mock import patch, Mock
from src.data.loaders.url_csv_loader import URLCSVLoader

@patch("requests.get")
def test_url_csv_loader(mock_get):
    csv_content = """DatGeracaoConjuntoDados;NomAgente;NumCPFCNPJ
2026-01-10;ENERGISA ACRE - DISTRIBUIDORA DE ENERGIA S.A;04065033000170
2026-01-11;ENERGISA ACRE - DISTRIBUIDORA DE ENERGIA S.A;04065033000171
"""

    mock_response = Mock()
    mock_response.text = csv_content
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    loader = URLCSVLoader("http://fakeurl.com/dados.csv")
    data = loader.load()

    assert isinstance(data, list)
    assert data == [
        {
            "DatGeracaoConjuntoDados": "2026-01-10",
            "NomAgente": "ENERGISA ACRE - DISTRIBUIDORA DE ENERGIA S.A",
            "NumCPFCNPJ": "04065033000170"
        },
        {
            "DatGeracaoConjuntoDados": "2026-01-11",
            "NomAgente": "ENERGISA ACRE - DISTRIBUIDORA DE ENERGIA S.A",
            "NumCPFCNPJ": "04065033000171"
        }
    ]
    assert loader.get_headers() == ["DatGeracaoConjuntoDados", "NomAgente", "NumCPFCNPJ"]