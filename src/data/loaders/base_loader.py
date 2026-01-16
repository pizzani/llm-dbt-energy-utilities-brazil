from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseLoader(ABC):
    """
    Classe mãe de todos os loaders de dados.
    Define a interface que todo loader deve implementar.
    """
    
    @abstractmethod
    def load(self, **kwargs) -> List[Dict[str, Any]]:
        """Carrega os dados e retorna lista de dicionários"""
        pass

    @abstractmethod
    def get_headers(self) -> List[str]:
        """Retorna os nomes das colunas/dados"""
        pass
    
    def preview(self, n: int = 5) -> List[Dict[str, Any]]:
        """Método opcional de preview das primeiras linhas"""
        data = self.load()
        return data[:n]