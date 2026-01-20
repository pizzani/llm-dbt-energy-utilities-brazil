import psycopg2
from psycopg2.extensions import connection
from typing import Optional
import logging

from src.config.database_config import DatabaseConfig

logger = logging.getLogger(__name__)


class DatabaseClient:
    
    def __init__(self, config=None):
        self.config = config or DatabaseConfig
        self._connection: Optional[connection] = None
    
    def connect(self) -> connection:
        if self._connection is None or self._connection.closed:
            try:
                self._connection = psycopg2.connect(
                    **self.config.get_connection_params()
                )
                logger.info(
                    f"Connected to: "
                    f"{self.config.host}/{self.config.database}"
                )
            except psycopg2.Error as e:
                logger.error(f"Failed to connect: {e}")
                raise
        
        return self._connection
    
    def disconnect(self):
        if self._connection and not self._connection.closed:
            self._connection.close()
            logger.info("Closed connection.")
            self._connection = None
    
    def is_connected(self) -> bool:
        return self._connection is not None and not self._connection.closed
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()