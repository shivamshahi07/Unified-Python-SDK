"""Cloudflare Workers deployment logic."""

import httpx
from typing import Dict, Any
from unified_serverless.providers.cloudflare.utils import get_api_token, get_account_id
from unified_serverless.utils.logger import get_logger

logger = get_logger(__name__)


def deploy_worker(function_name: str, worker_script: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deploy a worker script to Cloudflare.
    
    Args:
        function_name: Name of the worker
        worker_script: JavaScript worker code
        config: Deployment configuration
        
    Returns:
        Deployment result with URL and metadata
    """
    api_token = get_api_token()
    account_id = get_account_id()
    
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/scripts/{function_name}"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/javascript",
    }
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.put(url, content=worker_script, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            # Construct worker URL
            worker_url = f"https://{function_name}.workers.dev"
            
            return {
                "success": True,
                "function_name": function_name,
                "url": worker_url,
                "provider": "cloudflare",
                "metadata": result,
            }
    except httpx.HTTPError as e:
        logger.error(f"Deployment failed: {e}")
        raise RuntimeError(f"Failed to deploy to Cloudflare: {e}")
