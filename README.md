# Unified Serverless SDK

A unified Python SDK for deploying and interacting with serverless functions across multiple cloud providers.

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Architecture](https://img.shields.io/badge/architecture-Adapter%20Pattern-orange)](README.md)

<div align="center">
  <img src="assets/demo.gif" alt="Unified Serverless SDK Live Execution Demo" width="900px" style="border-radius: 8px; box-shadow: 0 8px 30px rgba(0,0,0,0.3);" />
</div>

## Features

- Deploy Python functions to multiple serverless providers
- Unified interface across all providers
- Easy to extend with new providers using the adapter pattern
- CLI for deployment and invocation
- Local development server for testing
- Type-safe configuration with Pydantic

## Installation

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick Start

### 1. Write a Function

Create a Python function:

```python
def hello(event):
    name = event.get("name", "world")
    return {"message": f"Hello {name}!"}
```

### 2. Deploy via SDK

```python
from unified_serverless import Function

fn = Function(hello)
result = fn.deploy(provider="cloudflare")
print(f"Deployed to: {result['url']}")
```

### 3. Deploy via CLI

```bash
# Set credentials
export CLOUDFLARE_API_TOKEN="your_token"
export CLOUDFLARE_ACCOUNT_ID="your_account_id"

# Deploy
unified deploy examples/hello_world.py --provider cloudflare

# Invoke
unified invoke hello --payload '{"name": "Alice"}'

# View logs
unified logs hello --provider cloudflare
```

### 4. Local Development

Test functions locally before deployment:

```bash
unified dev examples/hello_world.py
```

Then invoke at `http://localhost:8000/invoke`:

```bash
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'
```

## Supported Providers

- Cloudflare Workers (free tier available)

## Adding a New Provider

The SDK uses the adapter pattern to make adding providers simple:

1. Create a new directory: `unified_serverless/providers/<provider_name>/`
2. Implement the adapter: `adapter.py`

```python
from unified_serverless.core.provider_interface import ProviderInterface

class MyProviderAdapter(ProviderInterface):
    def deploy_function(self, function_object, config):
        # Implementation
        pass
    
    def invoke_function(self, function_name, payload):
        # Implementation
        pass
    
    def get_logs(self, function_name, limit=100):
        # Implementation
        pass
```

3. Register in `unified_serverless/providers/__init__.py`:

```python
from unified_serverless.providers.my_provider.adapter import MyProviderAdapter
from unified_serverless.core.provider_factory import ProviderFactory

ProviderFactory.register("my_provider", MyProviderAdapter)
```

That's it! No changes to core SDK code required.

## Architecture

```
unified_serverless/
├── core/              # Core abstractions
│   ├── function.py    # Function class
│   ├── config.py      # Configuration models
│   ├── provider_interface.py  # Adapter interface
│   └── provider_factory.py    # Provider registry
├── providers/         # Provider adapters
│   └── cloudflare/    # Cloudflare implementation
├── packaging/         # Function serialization
├── cli/              # CLI commands
└── utils/            # Utilities
```

## Configuration

Configure deployments using environment variables or the Config class:

```python
from unified_serverless import Function, Config

config = Config(
    provider="cloudflare",
    function_name="my_function",
    timeout=60,
    environment={"KEY": "value"}
)

fn = Function(hello, config)
fn.deploy()
```

## Testing

Run tests:

```bash
pytest
```

With coverage:

```bash
pytest --cov=unified_serverless
```

## Publishing to PyPI

```bash
python -m build
twine upload dist/*
```

## License

MIT License - see LICENSE file for details.
