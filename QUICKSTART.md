# Quick Start Guide

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the SDK
pip install -e .

# For development
pip install -e ".[dev]"
```

## Your First Function

### 1. Create a Function

Create `my_function.py`:

```python
def greet(event):
    name = event.get("name", "stranger")
    greeting = event.get("greeting", "Hello")
    return {
        "message": f"{greeting}, {name}!",
        "timestamp": "2026-03-17"
    }
```

### 2. Test Locally

Start the local development server:

```bash
unified dev my_function.py
```

In another terminal, test it:

```bash
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "greeting": "Hi"}'
```

### 3. Deploy to Cloudflare

Set up credentials:

```bash
export CLOUDFLARE_API_TOKEN="your_api_token_here"
export CLOUDFLARE_ACCOUNT_ID="your_account_id_here"
```

Deploy:

```bash
unified deploy my_function.py --provider cloudflare
```

### 4. Invoke the Deployed Function

```bash
unified invoke greet --payload '{"name": "Bob"}'
```

## Using the SDK Programmatically

```python
from unified_serverless import Function, Config

def my_function(event):
    return {"result": "success"}

# Simple deployment
fn = Function(my_function)
fn.deploy(provider="cloudflare")

# With configuration
config = Config(
    provider="cloudflare",
    function_name="my_custom_name",
    timeout=60
)
fn = Function(my_function, config)
fn.deploy()

# Invoke
result = fn.invoke({"key": "value"})
print(result)
```

## Getting Cloudflare Credentials

1. Go to https://dash.cloudflare.com
2. Navigate to "My Profile" → "API Tokens"
3. Create a token with "Workers Scripts:Edit" permission
4. Get your Account ID from the Workers dashboard

## Next Steps

- Check out `examples/` for more examples
- Read `ARCHITECTURE.md` to understand the design
- See `CONTRIBUTING.md` to add new providers
- Run tests: `pytest`

## Troubleshooting

### "Provider not found" error
Make sure you've imported the providers module. The SDK auto-registers providers on import.

### "Cannot extract source code" error
The function must be defined in a file (not in REPL). Use `def` syntax, not lambda.

### Deployment fails
- Verify credentials are set correctly
- Check network connectivity
- Review error messages for provider-specific issues

## CLI Reference

```bash
# Deploy
unified deploy <file.py> --provider cloudflare --name my_func

# Invoke
unified invoke <function_name> --payload '{"key": "value"}'

# Logs
unified logs <function_name> --provider cloudflare

# Local dev
unified dev <file.py> --port 8000
```
