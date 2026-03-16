"""Tests for local runtime."""

import pytest
from fastapi.testclient import TestClient
from unified_serverless.core.runtime import LocalRuntime


def test_local_runtime_initialization():
    """Test runtime initialization."""
    def sample_func(event):
        return {"result": "test"}
    
    runtime = LocalRuntime(sample_func)
    assert runtime.func == sample_func
    assert runtime.app is not None


def test_local_runtime_invoke():
    """Test function invocation through local runtime."""
    def sample_func(event):
        name = event.get("name", "world")
        return {"message": f"Hello {name}"}
    
    runtime = LocalRuntime(sample_func)
    client = TestClient(runtime.get_app())
    
    response = client.post("/invoke", json={"name": "Alice"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert data["result"]["message"] == "Hello Alice"


def test_local_runtime_root():
    """Test root endpoint."""
    def sample_func(event):
        return {}
    
    runtime = LocalRuntime(sample_func)
    client = TestClient(runtime.get_app())
    
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["function"] == "sample_func"


def test_local_runtime_error_handling():
    """Test error handling in local runtime."""
    def failing_func(event):
        raise ValueError("Test error")
    
    runtime = LocalRuntime(failing_func)
    client = TestClient(runtime.get_app())
    
    response = client.post("/invoke", json={})
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is False
    assert "Test error" in data["error"]
