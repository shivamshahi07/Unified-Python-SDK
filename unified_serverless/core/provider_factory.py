"""Factory for creating and managing provider adapters."""

from typing import Dict, Type
from unified_serverless.core.provider_interface import ProviderInterface


class ProviderFactory:
    """Factory for registering and retrieving provider adapters."""
    
    _providers: Dict[str, Type[ProviderInterface]] = {}
    
    @classmethod
    def register(cls, name: str, provider_class: Type[ProviderInterface]) -> None:
        """
        Register a provider adapter.
        
        Args:
            name: Provider identifier (e.g., 'cloudflare', 'aws', 'gcp')
            provider_class: Provider adapter class implementing ProviderInterface
        """
        cls._providers[name] = provider_class
    
    @classmethod
    def get(cls, name: str) -> ProviderInterface:
        """
        Get a provider adapter instance.
        
        Args:
            name: Provider identifier
            
        Returns:
            Instance of the provider adapter
            
        Raises:
            ValueError: If provider is not registered
        """
        if name not in cls._providers:
            raise ValueError(
                f"Provider '{name}' not found. Available providers: {list(cls._providers.keys())}"
            )
        return cls._providers[name]()
    
    @classmethod
    def list_providers(cls) -> list:
        """Return list of registered provider names."""
        return list(cls._providers.keys())
