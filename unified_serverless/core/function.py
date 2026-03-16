"""Function abstraction for deployable serverless functions."""

from typing import Callable, Dict, Any, Optional
from unified_serverless.core.config import Config
from unified_serverless.core.provider_factory import ProviderFactory
from unified_serverless.packaging.serializer import FunctionSerializer
from unified_serverless.packaging.bundler import FunctionBundler
from unified_serverless.utils.logger import get_logger

logger = get_logger(__name__)


class Function:
    """Represents a deployable serverless function."""
    
    def __init__(self, func: Callable, config: Optional[Config] = None):
        """
        Initialize a Function instance.
        
        Args:
            func: Python callable to deploy
            config: Optional configuration
        """
        self.func = func
        self.config = config or Config()
        self.metadata = FunctionSerializer.serialize(func)
        self.deployment_info: Optional[Dict[str, Any]] = None
        
        # Set function name in config if not provided
        if not self.config.function_name:
            self.config.function_name = self.metadata["name"]
    
    def deploy(self, provider: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Deploy the function to a serverless provider.
        
        Args:
            provider: Provider name (overrides config)
            **kwargs: Additional deployment configuration
            
        Returns:
            Deployment result
        """
        provider_name = provider or self.config.provider
        logger.info(f"Deploying function '{self.config.function_name}' to {provider_name}")
        
        # Get provider adapter
        adapter = ProviderFactory.get(provider_name)
        
        # Create deployment bundle
        bundle_path = FunctionBundler.create_bundle(self.metadata)
        
        # Prepare config
        deploy_config = self.config.model_dump()
        deploy_config.update(kwargs)
        deploy_config["bundle_path"] = bundle_path
        
        # Deploy
        self.deployment_info = adapter.deploy_function(self.metadata, deploy_config)
        logger.info(f"Deployment successful: {self.deployment_info.get('url', 'N/A')}")
        
        return self.deployment_info
    
    def invoke(self, payload: Dict[str, Any], provider: Optional[str] = None) -> Dict[str, Any]:
        """
        Invoke the deployed function.
        
        Args:
            payload: Input data for the function
            provider: Provider name (overrides config)
            
        Returns:
            Function execution result
        """
        provider_name = provider or self.config.provider
        adapter = ProviderFactory.get(provider_name)
        
        logger.info(f"Invoking function '{self.config.function_name}'")
        result = adapter.invoke_function(self.config.function_name, payload)
        
        return result
