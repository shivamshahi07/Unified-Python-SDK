"""Tests for Cloudflare adapter."""

import pytest
from unittest.mock import Mock, patch
from unified_serverless.providers.cloudflare.adapter import CloudflareAdapter


def test_cloudflare_adapter_initialization():
    """Test adapter initialization."""
    adapter = CloudflareAdapter()
    assert adapter.deployed_functions == {}


def test_worker_script_creation():
    """Test JavaScript worker script generation."""
    adapter = CloudflareAdapter()
    
    function_metadata = {
        "name": "test_func",
        "source_code": "def test_func(event): return event",
        "module_path": "__main__",
        "doc": "Test function",
    }
    
    script = adapter._create_worker_script(function_metadata)
    assert "addEventListener" in script
    assert "test_func" in script
    assert "handleRequest" in script


@patch.dict("os.environ", {"CLOUDFLARE_API_TOKEN": "test_token", "CLOUDFLARE_ACCOUNT_ID": "test_account"})
@patch("unified_serverless.providers.cloudflare.deploy.httpx.Client")
def test_deploy_function_success(mock_client):
    """Test successful function deployment."""
    # Mock HTTP response
    mock_response = Mock()
    mock_response.json.return_value = {"success": True}
    mock_response.raise_for_status = Mock()
    
    mock_context = Mock()
    mock_context.__enter__ = Mock(return_value=mock_context)
    mock_context.__exit__ = Mock(return_value=False)
    mock_context.put = Mock(return_value=mock_response)
    mock_client.return_value = mock_context
    
    adapter = CloudflareAdapter()
    
    function_metadata = {
        "name": "test_func",
        "source_code": "def test_func(event): return event",
        "module_path": "__main__",
        "doc": "Test",
    }
    
    config = {"function_name": "test_func"}
    
    result = adapter.deploy_function(function_metadata, config)
    
    assert result["success"] is True
    assert result["function_name"] == "test_func"
    assert "workers.dev" in result["url"]
