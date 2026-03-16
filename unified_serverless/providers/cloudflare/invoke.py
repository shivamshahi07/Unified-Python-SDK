"""Cloudflare Workers invocation logic."""

import httpx
from typing import Dict, Any
from unified_serverless.utils.logger import get_logger

logger = get_logger(__name__)


def invoke_worker(function_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Invoke a deployed Cloudflare Worker.
    
    Args:
        function_name: Name of the worker
        payload: Input data
        
    Returns:
        Worker execution result
    """
    worker_url = f"https://{function_name}.workers.dev"
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(worker_url, json=payload)
            response.raise_for_status()
            
            return {
                "success": True,
                "status_code": response.status_code,
                "result": response.json(),
            }
    except httpx.HTTPError as e:
        logger.error(f"Invocation failed: {e}")
        return {
            "success": False,
            "error": str(e),
        }
