"""Example serverless function."""

from unified_serverless import Function


def hello(event):
    """Simple hello world function."""
    name = event.get("name", "world")
    return {"message": f"Hello {name}!"}


if __name__ == "__main__":
    fn = Function(hello)
    fn.deploy(provider="cloudflare")
