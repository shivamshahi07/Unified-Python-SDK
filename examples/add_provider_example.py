"""
Example showing how easy it is to add a new provider.

This demonstrates the extensibility of the SDK architecture.
To add a real provider, you would:
1. Create the adapter file
2. Register it
3. Use it immediately
"""

from typing import Dict, Any, Optional
from unified_serverless.core.provider_interface import ProviderInterface
from unified_serverless.core.provider_factory import ProviderFactory
from unified_serverless import Function


# Step 1: Create a new adapter
class MockProviderAdapter(ProviderInterface):
    """Example adapter for a mock provider."""
    
    def deploy_function(self, function_object: Any, config: Dict[str, Any]) -> Dict[str, Any]:
        """Mock deployment."""
        function_name = config.get("function_name", function_object["name"])
        return {
            "success": True,
            "function_name": function_name,
            "url": f"https://{function_name}.mock-provider.com",
            "provider": "mock",
            "message": "Mock deployment successful"
        }
    
    def invoke_function(self, function_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Mock invocation."""
        return {
            "success": True,
            "result": {
                "message": "Mock invocation",
                "input": payload,
                "function": function_name
            }
        }
    
    def get_logs(self, function_name: str, limit: Optional[int] = 100) -> list:
        """Mock logs."""
        return [
            {"timestamp": "2026-03-17T10:00:00Z", "message": "Function started"},
            {"timestamp": "2026-03-17T10:00:01Z", "message": "Function completed"},
        ]


# Step 2: Register the provider
ProviderFactory.register("mock", MockProviderAdapter)


# Step 3: Use it immediately!
def my_function(event):
    """Example function."""
    return {"result": f"Processed: {event}"}


if __name__ == "__main__":
    # Verify registration
    print("Available providers:", ProviderFactory.list_providers())
    
    # Use the new provider
    fn = Function(my_function)
    
    # Deploy to mock provider
    result = fn.deploy(provider="mock")
    print(f"\nDeployment result: {result}")
    
    # Invoke
    invoke_result = fn.invoke({"test": "data"}, provider="mock")
    print(f"\nInvocation result: {invoke_result}")
    
    print("\n✓ New provider added and working with zero core code changes!")
