"""Main CLI entry point."""

import typer
from typing import Optional
from unified_serverless.cli.commands.deploy import deploy_command
from unified_serverless.cli.commands.invoke import invoke_command
from unified_serverless.cli.commands.logs import logs_command
import unified_serverless.providers  # Auto-register providers

app = typer.Typer(
    name="unified",
    help="Unified Serverless SDK - Deploy functions across multiple providers",
    add_completion=False,
)


@app.command("deploy")
def deploy(
    function_path: str = typer.Argument(..., help="Path to Python file containing the function"),
    provider: str = typer.Option("cloudflare", "--provider", "-p", help="Serverless provider"),
    function_name: Optional[str] = typer.Option(None, "--name", "-n", help="Function name"),
):
    """Deploy a function to a serverless provider."""
    deploy_command(function_path, provider, function_name)


@app.command("invoke")
def invoke(
    function_name: str = typer.Argument(..., help="Name of the deployed function"),
    payload: str = typer.Option("{}", "--payload", "-d", help="JSON payload"),
    provider: str = typer.Option("cloudflare", "--provider", "-p", help="Serverless provider"),
):
    """Invoke a deployed function."""
    invoke_command(function_name, payload, provider)


@app.command("logs")
def logs(
    function_name: str = typer.Argument(..., help="Name of the deployed function"),
    provider: str = typer.Option("cloudflare", "--provider", "-p", help="Serverless provider"),
    limit: int = typer.Option(100, "--limit", "-l", help="Maximum log entries"),
):
    """Retrieve logs for a deployed function."""
    logs_command(function_name, provider, limit)


@app.command("dev")
def dev(
    function_path: str = typer.Argument(..., help="Path to Python file containing the function"),
    port: int = typer.Option(8000, "--port", help="Port to run on"),
):
    """Run a function locally for development."""
    import uvicorn
    from unified_serverless.cli.commands.deploy import load_function_from_file
    from unified_serverless.core.runtime import LocalRuntime
    
    try:
        func = load_function_from_file(function_path)
        runtime = LocalRuntime(func)
        
        typer.echo(f"Starting local runtime for '{func.__name__}' on port {port}")
        typer.echo(f"Invoke at: http://localhost:{port}/invoke")
        
        uvicorn.run(runtime.get_app(), host="0.0.0.0", port=port)
        
    except Exception as e:
        typer.echo(f"✗ Failed to start dev server: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
