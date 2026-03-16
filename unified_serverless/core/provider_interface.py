"""Provider interface defining the adapter pattern for serverless providers."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class ProviderInterface(ABC):
    """Abstract base class that all serverless providers must implement."""

    @abstractmethod
    def deploy_function(self, function_object: Any, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deploy a function to the serverless provider.
        
        Args:
            function_object: The function metadata and code to deploy
            config: Provider-specific configuration
            
        Returns:
            Deployment result containing URL, function ID, etc.
        """
        pass

    @abstractmethod
    def invoke_function(self, function_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke a deployed function.
        
        Args:
            function_name: Name or identifier of the function
            payload: Input data for the function
            
        Returns:
            Function execution result
        """
        pass

    @abstractmethod
    def get_logs(self, function_name: str, limit: Optional[int] = 100) -> list:
        """
        Retrieve logs for a deployed function.
        
        Args:
            function_name: Name or identifier of the function
            limit: Maximum number of log entries to retrieve
            
        Returns:
            List of log entries
        """
        pass
