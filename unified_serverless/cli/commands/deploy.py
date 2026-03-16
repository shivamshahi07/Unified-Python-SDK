"""Deploy command implementation."""

import sys
import importlib.util
from pathlib import Path
from typing import Optional
import typer
from unified_serverless.core.function import Function
from unified_serverless.core.config import Config
from unified_serverless.utils.logger import get_logger

logger = get_logger(__name__)


def deploy_command(
    function_path: str,
    provider: str = "cloudflare",
    function_name: Optional[str] = None,
) -> None:
    """
    Deploy a function to a serverless provider.
    
    Args:
        function_path: Path to Python file containing the function
        provider: Provider name
        function_name: Optional function name override
    """
    try:
        # Load the function from file
        func = load_function_from_file(function_path)
        
        # Create config
        config = Config(provider=provider, function_name=function_name)
        
        # Deploy
        fn = Function(func, config)
        result = fn.deploy()
        
        typer.echo(f"✓ Deployment successful!")
        typer.echo(f"  Function: {result['function_name']}")
        typer.echo(f"  Provider: {result['provider']}")
        typer.echo(f"  URL: {result['url']}")
        
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        typer.echo(f"✗ Deployment failed: {e}", err=True)
        raise typer.Exit(1)


def load_function_from_file(file_path: str):
    """Load a function from a Python file."""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Load module
    spec = importlib.util.spec_from_file_location("user_function", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["user_function"] = module
    spec.loader.exec_module(module)
    
    # Find the first function in the module
    for name in dir(module):
        obj = getattr(module, name)
        if callable(obj) and not name.startswith("_") and hasattr(obj, "__code__"):
            return obj
    
    raise ValueError(f"No function found in {file_path}")
