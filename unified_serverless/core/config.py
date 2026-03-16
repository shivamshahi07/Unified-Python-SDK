"""Configuration models for the SDK."""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class Config(BaseModel):
    """Configuration for serverless function deployment."""
    
    model_config = ConfigDict(extra="allow")
    
    provider: str = Field(default="cloudflare", description="Serverless provider name")
    function_name: Optional[str] = Field(default=None, description="Name of the function")
    region: Optional[str] = Field(default=None, description="Deployment region")
    memory: Optional[int] = Field(default=128, description="Memory allocation in MB")
    timeout: Optional[int] = Field(default=30, description="Timeout in seconds")
    environment: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    provider_config: Dict[str, Any] = Field(default_factory=dict, description="Provider-specific config")
