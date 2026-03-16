#!/usr/bin/env python3
"""
Interactive Cloudflare Deployment Script

This script guides you through deploying your first function to Cloudflare Workers.
"""

import os
import sys


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70)


def print_step(number, text):
    """Print a step header."""
    print(f"\n[Step {number}] {text}")


def check_uv():
    """Check if uv is installed."""
    import subprocess
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✓ uv is installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("  ✗ uv is not installed")
    print("\n  Install uv:")
    print("    curl -LsSf https://astral.sh/uv/install.sh | sh")
    print("    # or")
    print("    pip install uv")
    return False


def check_credentials():
    """Check and prompt for credentials."""
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    
    if not token:
        print("\n  ❌ CLOUDFLARE_API_TOKEN not set")
        print("\n  How to get your API token:")
        print("    1. Go to: https://dash.cloudflare.com/profile/api-tokens")
        print("    2. Click 'Create Token'")
        print("    3. Use 'Edit Cloudflare Workers' template")
        print("    4. Copy the token")
        print("\n  Then set it:")
        print("    export CLOUDFLARE_API_TOKEN='your_token_here'")
        return False
    
    if not account_id:
        print("\n  ❌ CLOUDFLARE_ACCOUNT_ID not set")
        print("\n  How to get your Account ID:")
        print("    1. Go to: https://dash.cloudflare.com")
        print("    2. Click 'Workers & Pages'")
        print("    3. Copy the Account ID from the right side")
        print("\n  Then set it:")
        print("    export CLOUDFLARE_ACCOUNT_ID='your_account_id_here'")
        return False
    
    print(f"  ✓ CLOUDFLARE_API_TOKEN: {token[:8]}...{token[-4:]}")
    print(f"  ✓ CLOUDFLARE_ACCOUNT_ID: {account_id}")
    return True


def test_local():
    """Test function locally."""
    print("\n  Testing function locally first...")
    print("  Starting local dev server on port 8000...")
    print("\n  In another terminal, run:")
    print("    curl -X POST http://localhost:8000/invoke \\")
    print("      -H 'Content-Type: application/json' \\")
    print("      -d '{\"city\": \"San Francisco\"}'")
    print("\n  Press Ctrl+C when done testing")
    print("\n  To skip local testing and deploy directly, press Ctrl+C now")
    
    try:
        import subprocess
        subprocess.run([
            "uv", "run", "unified", "dev", 
            "examples/real_cloudflare_deployment.py"
        ])
    except KeyboardInterrupt:
        print("\n  Skipping local test...")


def deploy():
    """Deploy to Cloudflare."""
    print("\n  Deploying to Cloudflare Workers...")
    print("  This will make an API call to Cloudflare...")
    
    import subprocess
    result = subprocess.run([
        "uv", "run", "python", 
        "examples/real_cloudflare_deployment.py"
    ])
    
    return result.returncode == 0


def main():
    """Main interactive workflow."""
    print_header("CLOUDFLARE WORKERS DEPLOYMENT GUIDE")
    
    print("\nThis script will help you deploy your first serverless function")
    print("to Cloudflare Workers using the Unified Serverless SDK.")
    
    # Step 1: Check uv
    print_step(1, "Checking dependencies")
    if not check_uv():
        sys.exit(1)
    
    # Step 2: Install SDK
    print_step(2, "Installing SDK")
    print("  Running: uv sync")
    import subprocess
    result = subprocess.run(["uv", "sync"], capture_output=True)
    if result.returncode == 0:
        print("  ✓ SDK installed")
    else:
        print("  ✗ Installation failed")
        sys.exit(1)
    
    # Step 3: Check credentials
    print_step(3, "Checking Cloudflare credentials")
    if not check_credentials():
        print("\n  Please set your credentials and run this script again.")
        sys.exit(1)
    
    # Step 4: Ask about local testing
    print_step(4, "Local testing (optional)")
    response = input("\n  Test locally before deploying? (y/n): ").lower()
    if response == 'y':
        test_local()
    
    # Step 5: Deploy
    print_step(5, "Deploying to Cloudflare")
    response = input("\n  Ready to deploy? (y/n): ").lower()
    if response != 'y':
        print("\n  Deployment cancelled.")
        sys.exit(0)
    
    if deploy():
        print_header("SUCCESS!")
        print("\nYour function is now live on Cloudflare Workers!")
        print("\nNext steps:")
        print("  1. Visit Cloudflare dashboard to see your worker")
        print("  2. Test invocation with the CLI")
        print("  3. Try deploying your own functions")
        print("\nUseful commands:")
        print("  uv run unified invoke weather_api --payload '{\"city\": \"Tokyo\"}'")
        print("  uv run unified logs weather_api")
    else:
        print_header("DEPLOYMENT FAILED")
        print("\nCheck the error messages above for details.")
        print("See WALKTHROUGH.md for troubleshooting tips.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDeployment cancelled by user.")
        sys.exit(0)
