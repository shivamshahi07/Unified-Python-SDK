"""Integration tests for end-to-end workflows."""

import pytest
from unittest.mock import Mock, patch
from unified_serverless import Function, Config
from unified_serverless.core.provider_factory import ProviderFactory


def test_end_to_end_workflow():
    """Test complete workflow from function creation to invocation."""
    
    def sample_function(event):
        """Sample function for testing."""
        value = event.get("value", 0)
        return {"result": value * 2}
    
    # Create function
    fn = Function(sample_function)
    
    # Verify metadata
    assert fn.metadata["name"] == "sample_function"
    assert "def sample_function" in fn.metadata["source_code"]
    
    # Verify config
    assert fn.config.provider == "cloudflare"
    assert fn.config.function_name == "sample_function"


def test_provider_registration_workflow():
    """Test provider registration and retrieval."""
    
    # Verify cloudflare is registered
    providers = ProviderFactory.list_providers()
    assert "cloudflare" in providers
    
    # Get provider
    provider = ProviderFactory.get("cloudflare")
    assert provider is not None


def test_custom_config_workflow():
    """Test workflow with custom configuration."""
    
    def custom_func(event):
        return {"custom": True}
    
    config = Config(
        provider="cloudflare",
        function_name="my_custom_function",
        timeout=120,
        memory=512,
        environment={"KEY": "value"}
    )
    
    fn = Function(custom_func, config)
    
    assert fn.config.function_name == "my_custom_function"
    assert fn.config.timeout == 120
    assert fn.config.memory == 512
    assert fn.config.environment["KEY"] == "value"


@patch("unified_serverless.core.function.ProviderFactory.get")
@patch("unified_serverless.core.function.FunctionBundler.create_bundle")
def test_deploy_invoke_workflow(mock_bundle, mock_get_provider):
    """Test complete deploy and invoke workflow."""
    
    def workflow_func(event):
        return {"status": "success"}
    
    # Mock provider
    mock_provider = Mock()
    mock_provider.deploy_function.return_value = {
        "success": True,
        "function_name": "workflow_func",
        "url": "https://workflow_func.workers.dev",
        "provider": "cloudflare"
    }
    mock_provider.invoke_function.return_value = {
        "success": True,
        "result": {"status": "success"}
    }
    mock_get_provider.return_value = mock_provider
    mock_bundle.return_value = "/tmp/bundle"
    
    # Create and deploy
    fn = Function(workflow_func)
    deploy_result = fn.deploy()
    
    assert deploy_result["success"] is True
    assert deploy_result["url"] == "https://workflow_func.workers.dev"
    
    # Invoke
    invoke_result = fn.invoke({"test": "data"})
    
    assert invoke_result["success"] is True
    assert invoke_result["result"]["status"] == "success"
