import pytest
from unittest.mock import Mock, patch, MagicMock
from src.config.database_client import DatabaseClient
from src.config.database_config import DatabaseConfig


@pytest.fixture
def mock_config():
    config = DatabaseConfig()
    config.host = 'localhost'
    config.port = 5433
    config.database = 'test_db'
    config.user = 'test_user'
    config.password = 'test_pass'
    return config


@pytest.fixture
def db_client(mock_config):
    return DatabaseClient(config=mock_config)


class TestDatabaseClient:
    
    def test_init_with_default_config(self):
        client = DatabaseClient()
        assert client.config is not None
        assert client._connection is None
    
    def test_init_with_custom_config(self, mock_config):
        client = DatabaseClient(config=mock_config)
        assert client.config == mock_config
        assert client.config.host == 'localhost'
    
    @patch('psycopg2.connect')
    def test_connect_success(self, mock_connect, db_client):
        mock_conn = MagicMock()
        mock_conn.closed = False
        mock_connect.return_value = mock_conn
        
        connection = db_client.connect()
        
        assert connection is not None
        assert db_client.is_connected()
        mock_connect.assert_called_once()
    
    @patch('psycopg2.connect')
    def test_connect_reuses_existing_connection(self, mock_connect, db_client):
        mock_conn = MagicMock()
        mock_conn.closed = False
        mock_connect.return_value = mock_conn
        
        conn1 = db_client.connect()

        conn2 = db_client.connect()
        
        assert conn1 == conn2

        mock_connect.assert_called_once()
    
    @patch('psycopg2.connect')
    def test_connect_failure(self, mock_connect, db_client):
        import psycopg2
        mock_connect.side_effect = psycopg2.OperationalError("Connection failed")
        
        with pytest.raises(psycopg2.OperationalError):
            db_client.connect()
    
    @patch('psycopg2.connect')
    def test_disconnect(self, mock_connect, db_client):
        mock_conn = MagicMock()
        mock_conn.closed = False
        mock_connect.return_value = mock_conn
        
        db_client.connect()
        assert db_client.is_connected()
        
        db_client.disconnect()
        
        mock_conn.close.assert_called_once()
        assert db_client._connection is None
    
    @patch('psycopg2.connect')
    def test_is_connected_false_when_not_connected(self, mock_connect, db_client):
        assert not db_client.is_connected()
    
    @patch('psycopg2.connect')
    def test_context_manager(self, mock_connect, db_client):
        mock_conn = MagicMock()
        mock_conn.closed = False
        mock_connect.return_value = mock_conn
        
        with db_client as client:
            assert client.is_connected()
        
        mock_conn.close.assert_called_once()