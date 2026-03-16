# Contributing to Unified Serverless SDK

## Adding a New Provider

The SDK is designed to make adding new providers straightforward using the adapter pattern. Here's how to add support for a new serverless platform.

### Step 1: Create Provider Directory

Create a new directory under `unified_serverless/providers/`:

```
unified_serverless/providers/
└── your_provider/
    ├── __init__.py
    ├── adapter.py
    ├── deploy.py
    ├── invoke.py
    └── utils.py
```

### Step 2: Implement the Adapter

Create `adapter.py` that implements `ProviderInterface`:

```python
from typing import Dict, Any, Optional
from unified_serverless.core.provider_interface import ProviderInterface

class YourProviderAdapter(ProviderInterface):
    """Adapter for Your Provider."""
    
    def deploy_function(self, function_object: Any, config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy function to your provider."""
        # Your deployment logic here
        return {
            "success": True,
            "function_name": config["function_name"],
            "url": "https://your-function-url.com",
            "provider": "your_provider",
        }
    
    def invoke_function(self, function_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke deployed function."""
        # Your invocation logic here
        return {"success": True, "result": {}}
    
    def get_logs(self, function_name: str, limit: Optional[int] = 100) -> list:
        """Retrieve function logs."""
        # Your log retrieval logic here
        return []
```

### Step 3: Register the Provider

Add registration to `unified_serverless/providers/__init__.py`:

```python
from unified_serverless.providers.your_provider.adapter import YourProviderAdapter
from unified_serverless.core.provider_factory import ProviderFactory

ProviderFactory.register("your_provider", YourProviderAdapter)
```

### Step 4: Add Tests

Create `tests/test_your_provider_adapter.py`:

```python
import pytest
from unified_serverless.providers.your_provider.adapter import YourProviderAdapter

def test_your_provider_initialization():
    adapter = YourProviderAdapter()
    assert adapter is not None

# Add more tests...
```

### Step 5: Update Documentation

Add your provider to the README.md supported providers list.

## Development Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
pytest --cov=unified_serverless  # With coverage
```

## Code Style

We use:
- Black for formatting
- Ruff for linting
- Type hints throughout

Format code:
```bash
black unified_serverless tests
ruff check unified_serverless tests
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests
5. Ensure all tests pass
6. Submit a pull request

## Questions?

Open an issue on GitHub for questions or discussions.
