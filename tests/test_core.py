"""Tests for core functionality."""

import pytest
from unified_serverless.core.config import Config
from unified_serverless.core.provider_factory import ProviderFactory
from unified_serverless.packaging.serializer import FunctionSerializer


def test_config_creation():
    """Test configuration model."""
    config = Config(provider="cloudflare", function_name="test_func")
    assert config.provider == "cloudflare"
    assert config.function_name == "test_func"
    assert config.timeout == 30


def test_function_serialization():
    """Test function serialization."""
    def sample_func(event):
        return {"result": "test"}
    
    metadata = FunctionSerializer.serialize(sample_func)
    assert metadata["name"] == "sample_func"
    assert "def sample_func" in metadata["source_code"]
    assert "result" in metadata["source_code"]


def test_provider_factory_registration():
    """Test provider registration and retrieval."""
    from unified_serverless.providers.cloudflare.adapter import CloudflareAdapter
    
    # Register provider
    ProviderFactory.register("test_cloudflare", CloudflareAdapter)
    
    # Retrieve provider
    provider = ProviderFactory.get("test_cloudflare")
    assert isinstance(provider, CloudflareAdapter)


def test_provider_factory_invalid():
    """Test provider factory with invalid provider."""
    with pytest.raises(ValueError, match="Provider 'invalid' not found"):
        ProviderFactory.get("invalid")


def test_provider_list():
    """Test listing registered providers."""
    providers = ProviderFactory.list_providers()
    assert isinstance(providers, list)
    assert "cloudflare" in providers
