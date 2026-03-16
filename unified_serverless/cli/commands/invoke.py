"""Invoke command implementation."""

import json
from typing import Optional
import typer
from unified_serverless.core.provider_factory import ProviderFactory
from unified_serverless.utils.logger import get_logger

logger = get_logger(__name__)


def invoke_command(
    function_name: str,
    payload: str = "{}",
    provider: str = "cloudflare",
) -> None:
    """
    Invoke a deployed function.
    
    Args:
        function_name: Name of the deployed function
        payload: JSON payload to send
        provider: Provider name
    """
    try:
        # Parse payload
        payload_dict = json.loads(payload)
        
        # Get provider and invoke
        adapter = ProviderFactory.get(provider)
        result = adapter.invoke_function(function_name, payload_dict)
        
        typer.echo("✓ Invocation successful!")
        typer.echo(json.dumps(result, indent=2))
        
    except json.JSONDecodeError as e:
        typer.echo(f"✗ Invalid JSON payload: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        logger.error(f"Invocation failed: {e}")
        typer.echo(f"✗ Invocation failed: {e}", err=True)
        raise typer.Exit(1)
