"""Provider adapters for different serverless platforms."""

# Auto-register providers
from unified_serverless.providers.cloudflare.adapter import CloudflareAdapter
from unified_serverless.core.provider_factory import ProviderFactory

ProviderFactory.register("cloudflare", CloudflareAdapter)
