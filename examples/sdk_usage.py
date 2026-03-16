"""Example showing programmatic SDK usage."""

from unified_serverless import Function, Config


def calculator(event):
    """A simple calculator function."""
    a = event.get("a", 0)
    b = event.get("b", 0)
    operation = event.get("op", "add")
    
    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else "Error: Division by zero"
    }
    
    result = operations.get(operation, "Unknown operation")
    
    return {
        "a": a,
        "b": b,
        "operation": operation,
        "result": result
    }


def main():
    """Main execution."""
    # Create configuration
    config = Config(
        provider="cloudflare",
        function_name="calculator",
        timeout=30
    )
    
    # Create function instance
    fn = Function(calculator, config)
    
    # Deploy
    print("Deploying function...")
    deployment_result = fn.deploy()
    print(f"✓ Deployed to: {deployment_result['url']}")
    
    # Invoke
    print("\nInvoking function...")
    test_cases = [
        {"a": 10, "b": 5, "op": "add"},
        {"a": 10, "b": 5, "op": "multiply"},
        {"a": 10, "b": 5, "op": "divide"},
    ]
    
    for test in test_cases:
        result = fn.invoke(test)
        print(f"  {test} -> {result}")


if __name__ == "__main__":
    main()
