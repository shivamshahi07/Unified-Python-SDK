"""Unified Serverless SDK - Deploy and invoke serverless functions across multiple providers."""

from unified_serverless.core.function import Function
from unified_serverless.core.config import Config

# Auto-register providers
import unified_serverless.providers

__version__ = "0.1.0"
__all__ = ["Function", "Config"]
