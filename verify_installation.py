#!/usr/bin/env python3
"""Verification script to ensure the SDK is properly installed."""

import sys


def verify_imports():
    """Verify all imports work."""
    print("Checking imports...")
    try:
        from unified_serverless import Function, Config
        from unified_serverless.core.provider_factory import ProviderFactory
        print("✓ Core imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def verify_providers():
    """Verify providers are registered."""
    print("\nChecking provider registration...")
    try:
        from unified_serverless.core.provider_factory import ProviderFactory
        providers = ProviderFactory.list_providers()
        
        if "cloudflare" in providers:
            print(f"✓ Providers registered: {providers}")
            return True
        else:
            print(f"✗ Cloudflare provider not found. Available: {providers}")
            return False
    except Exception as e:
        print(f"✗ Provider check failed: {e}")
        return False


def verify_function_creation():
    """Verify Function class works."""
    print("\nChecking Function class...")
    try:
        from unified_serverless import Function
        
        def test_func(event):
            return {"test": "success"}
        
        fn = Function(test_func)
        assert fn.metadata["name"] == "test_func"
        print("✓ Function class working")
        return True
    except Exception as e:
        print(f"✗ Function class failed: {e}")
        return False


def verify_cli():
    """Verify CLI is available."""
    print("\nChecking CLI availability...")
    import subprocess
    try:
        result = subprocess.run(
            ["unified", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and "Unified Serverless SDK" in result.stdout:
            print("✓ CLI command available")
            return True
        else:
            print("✗ CLI command not working properly")
            return False
    except FileNotFoundError:
        print("✗ CLI command not found in PATH")
        return False
    except Exception as e:
        print(f"✗ CLI check failed: {e}")
        return False


def main():
    """Run all verification checks."""
    print("=" * 50)
    print("Unified Serverless SDK - Installation Verification")
    print("=" * 50)
    
    checks = [
        verify_imports(),
        verify_providers(),
        verify_function_creation(),
        verify_cli(),
    ]
    
    print("\n" + "=" * 50)
    if all(checks):
        print("✓ All checks passed! SDK is ready to use.")
        print("=" * 50)
        return 0
    else:
        print("✗ Some checks failed. Please review the output above.")
        print("=" * 50)
        return 1


if __name__ == "__main__":
    sys.exit(main())
