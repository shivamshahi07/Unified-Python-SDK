"""Function serialization utilities."""

import inspect
from typing import Callable, Dict, Any


class FunctionSerializer:
    """Serializes Python functions for deployment."""
    
    @staticmethod
    def serialize(func: Callable) -> Dict[str, Any]:
        """
        Extract function metadata and source code.
        
        Args:
            func: Python callable to serialize
            
        Returns:
            Dictionary containing function metadata
        """
        try:
            source_code = inspect.getsource(func)
        except (OSError, TypeError):
            raise ValueError(f"Cannot extract source code for function {func.__name__}")
        
        module_path = inspect.getmodule(func).__name__ if inspect.getmodule(func) else "__main__"
        
        return {
            "name": func.__name__,
            "source_code": source_code,
            "module_path": module_path,
            "doc": func.__doc__ or "",
        }
