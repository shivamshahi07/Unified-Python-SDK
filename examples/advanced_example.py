"""Advanced example showing SDK features."""

from unified_serverless import Function, Config


def process_data(event):
    """Process data with validation."""
    data = event.get("data", [])
    operation = event.get("operation", "sum")
    
    if not isinstance(data, list):
        return {"error": "data must be a list"}
    
    if operation == "sum":
        result = sum(data)
    elif operation == "average":
        result = sum(data) / len(data) if data else 0
    elif operation == "max":
        result = max(data) if data else None
    else:
        return {"error": f"Unknown operation: {operation}"}
    
    return {
        "operation": operation,
        "result": result,
        "count": len(data)
    }


if __name__ == "__main__":
    # Create custom configuration
    config = Config(
        provider="cloudflare",
        function_name="data_processor",
        timeout=60,
        environment={"ENV": "production"}
    )
    
    # Deploy with config
    fn = Function(process_data, config)
    deployment = fn.deploy()
    
    print(f"Deployed to: {deployment['url']}")
    
    # Test invocation
    result = fn.invoke({"data": [1, 2, 3, 4, 5], "operation": "sum"})
    print(f"Result: {result}")
