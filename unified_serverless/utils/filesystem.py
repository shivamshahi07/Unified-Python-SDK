"""Filesystem utilities."""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional


def create_temp_dir(prefix: str = "unified_serverless_") -> str:
    """Create a temporary directory."""
    return tempfile.mkdtemp(prefix=prefix)


def cleanup_temp_dir(path: str) -> None:
    """Remove a temporary directory and its contents."""
    if os.path.exists(path):
        shutil.rmtree(path)


def ensure_dir(path: str) -> None:
    """Ensure a directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)


def read_file(path: str) -> str:
    """Read file contents."""
    with open(path, 'r') as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    """Write content to file."""
    with open(path, 'w') as f:
        f.write(content)
