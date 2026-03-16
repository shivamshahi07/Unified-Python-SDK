"""Local development runtime for testing functions."""

from typing import Callable, Dict, Any
from fastapi import FastAPI, Request
from unified_serverless.utils.logger import get_logger

logger = get_logger(__name__)


class LocalRuntime:
    """Local development server for testing functions."""
    
    def __init__(self, func: Callable):
        """
        Initialize local runtime with a function.
        
        Args:
            func: Python callable to run locally
        """
        self.func = func
        self.app = FastAPI(title="Unified Serverless Local Runtime")
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup FastAPI routes."""
        
        @self.app.get("/")
        async def root():
            return {
                "message": "Unified Serverless Local Runtime",
                "function": self.func.__name__,
            }
        
        @self.app.post("/invoke")
        async def invoke(request: Request):
            """Invoke the function with JSON payload."""
            try:
                payload = await request.json()
                result = self.func(payload)
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Function execution failed: {e}")
                return {"success": False, "error": str(e)}
    
    def get_app(self) -> FastAPI:
        """Get the FastAPI application instance."""
        return self.app
