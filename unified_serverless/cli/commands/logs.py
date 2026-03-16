"""Logs command implementation."""

import json
import typer
from unified_serverless.core.provider_factory import ProviderFactory
from unified_serverless.utils.logger import get_logger

logger = get_logger(__name__)


def logs_command(
    function_name: str,
    provider: str = "cloudflare",
    limit: int = 100,
) -> None:
    """
    Retrieve logs for a deployed function.
    
    Args:
        function_name: Name of the deployed function
        provider: Provider name
        limit: Maximum number of log entries
    """
    try:
        adapter = ProviderFactory.get(provider)
        logs = adapter.get_logs(function_name, limit=limit)
        
        typer.echo(f"Logs for '{function_name}':")
        typer.echo(json.dumps(logs, indent=2))
        
    except Exception as e:
        logger.error(f"Failed to retrieve logs: {e}")
        typer.echo(f"✗ Failed to retrieve logs: {e}", err=True)
        raise typer.Exit(1)
