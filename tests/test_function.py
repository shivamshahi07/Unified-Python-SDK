"""Tests for Function class."""

import pytest
from unittest.mock import Mock, patch
from unified_serverless import Function, Config


def test_function_initialization():
    """Test Function initialization."""
    def sample_func(event):
        return {"result": "test"}
    
    fn = Function(sample_func)
    assert fn.func == sample_func
    assert fn.config.provider == "cloudflare"
    assert fn.metadata["name"] == "sample_func"


def test_function_with_config():
    """Test Function with custom config."""
    def sample_func(event):
        return {}
    
    config = Config(provider="cloudflare", function_name="custom_name")
    fn = Function(sample_func, config)
    
    assert fn.config.function_name == "custom_name"
    assert fn.config.provider == "cloudflare"


@patch("unified_serverless.core.function.ProviderFactory.get")
@patch("unified_serverless.core.function.FunctionBundler.create_bundle")
def test_function_deploy(mock_bundle, mock_get_provider):
    """Test function deployment."""
    def sample_func(event):
        return {}
    
    # Mock provider
    mock_provider = Mock()
    mock_provider.deploy_function.return_value = {
        "success": True,
        "function_name": "sample_func",
        "url": "https://test.workers.dev",
        "provider": "cloudflare"
    }
    mock_get_provider.return_value = mock_provider
    
    # Mock bundler
    mock_bundle.return_value = "/tmp/bundle"
    
    fn = Function(sample_func)
    result = fn.deploy()
    
    assert result["success"] is True
    assert result["function_name"] == "sample_func"
    assert mock_provider.deploy_function.called


@patch("unified_serverless.core.function.ProviderFactory.get")
def test_function_invoke(mock_get_provider):
    """Test function invocation."""
    def sample_func(event):
        return {}
    
    # Mock provider
    mock_provider = Mock()
    mock_provider.invoke_function.return_value = {
        "success": True,
        "result": {"message": "test"}
    }
    mock_get_provider.return_value = mock_provider
    
    fn = Function(sample_func)
    result = fn.invoke({"test": "data"})
    
    assert result["success"] is True
    assert mock_provider.invoke_function.called
