"""Function bundling utilities."""

import json
import os
from typing import Dict, Any
from unified_serverless.utils.filesystem import create_temp_dir, write_file


class FunctionBundler:
    """Creates deployable artifacts from serialized functions."""
    
    @staticmethod
    def create_bundle(function_metadata: Dict[str, Any], requirements: list = None) -> str:
        """
        Create a deployable bundle containing function code and metadata.
        
        Args:
            function_metadata: Serialized function data
            requirements: List of Python package requirements
            
        Returns:
            Path to the bundle directory
        """
        bundle_dir = create_temp_dir()
        
        # Create handler.py with the function code
        handler_code = f"""
{function_metadata['source_code']}

def handler(event):
    \"\"\"Entry point for serverless execution.\"\"\"
    return {function_metadata['name']}(event)
"""
        write_file(os.path.join(bundle_dir, "handler.py"), handler_code)
        
        # Create requirements.txt
        requirements_content = "\n".join(requirements or [])
        write_file(os.path.join(bundle_dir, "requirements.txt"), requirements_content)
        
        # Create metadata.json
        metadata = {
            "function_name": function_metadata["name"],
            "module_path": function_metadata["module_path"],
            "doc": function_metadata["doc"],
        }
        write_file(os.path.join(bundle_dir, "metadata.json"), json.dumps(metadata, indent=2))
        
        return bundle_dir
