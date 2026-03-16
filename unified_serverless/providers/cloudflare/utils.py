"""Cloudflare-specific utilities."""

import os
from typing import Optional


def get_api_token() -> Optional[str]:
    """Get Cloudflare API token from environment."""
    return os.environ.get("CLOUDFLARE_API_TOKEN")


def get_account_id() -> Optional[str]:
    """Get Cloudflare account ID from environment."""
    return os.environ.get("CLOUDFLARE_ACCOUNT_ID")


def validate_credentials() -> None:
    """Validate that required Cloudflare credentials are present."""
    if not get_api_token():
        raise ValueError("CLOUDFLARE_API_TOKEN environment variable is required")
    if not get_account_id():
        raise ValueError("CLOUDFLARE_ACCOUNT_ID environment variable is required")
