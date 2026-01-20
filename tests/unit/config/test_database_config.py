import pytest
from src.config.database_config import DatabaseConfig

def test_database_config_defaults():
    config = DatabaseConfig()
    assert config.host is not None
    assert config.port == 5433
    assert isinstance(config.get_connection_params(), dict)

def test_database_config_params():
    config = DatabaseConfig()
    params = config.get_connection_params()
    
    assert 'host' in params
    assert 'port' in params
    assert 'database' in params
    assert 'user' in params
    assert 'password' in params