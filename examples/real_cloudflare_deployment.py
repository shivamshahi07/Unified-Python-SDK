#!/usr/bin/env python3
"""
Real Cloudflare Workers Deployment Example

This example shows how to actually deploy a function to Cloudflare Workers.

PREREQUISITES:
1. Cloudflare account (free tier works)
2. API Token with Workers Scripts:Edit permission
3. Account ID from Cloudflare dashboard

SETUP:
1. Get your API token:
   - Go to https://dash.cloudflare.com/profile/api-tokens
   - Click "Create Token"
   - Use "Edit Cloudflare Workers" template
   - Copy the token

2. Get your Account ID:
   - Go to https://dash.cloudflare.com
   - Click on "Workers & Pages"
   - Your Account ID is shown on the right side

3. Set environment variables:
   export CLOUDFLARE_API_TOKEN="your_token_here"
   export CLOUDFLARE_ACCOUNT_ID="your_account_id_here"

USAGE:
   python3 examples/real_cloudflare_deployment.py
"""

import os
import sys
from unified_serverless import Function, Config


def weather_api(event):
    """
    A simple weather API function.
    
    This function accepts a city name and returns mock weather data.
    In a real scenario, you'd call an actual weather API.
    """
    city = event.get("city", "Unknown")
    
    # Mock weather data
    weather_data = {
        "city": city,
        "temperature": 72,
        "condition": "Sunny",
        "humidity": 45,
        "wind_speed": 10,
        "forecast": "Clear skies expected"
    }
    
    return {
        "success": True,
        "data": weather_data,
        "message": f"Weather data for {city}"
    }


def check_credentials():
    """Check if Cloudflare credentials are set."""
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    
    if not token or not account_id:
        print("❌ ERROR: Cloudflare credentials not set!")
        print("\nPlease set the following environment variables:")
        print("  export CLOUDFLARE_API_TOKEN='your_token_here'")
        print("  export CLOUDFLARE_ACCOUNT_ID='your_account_id_here'")
        print("\nHow to get credentials:")
        print("  1. API Token: https://dash.cloudflare.com/profile/api-tokens")
        print("  2. Account ID: https://dash.cloudflare.com (Workers & Pages section)")
        sys.exit(1)
    
    print("✓ Credentials found")
    print(f"  Account ID: {account_id[:8]}...")
    print(f"  API Token: {token[:8]}...")
    return True


def main():
    """Main deployment workflow."""
    print("=" * 70)
    print("CLOUDFLARE WORKERS DEPLOYMENT - REAL EXAMPLE")
    print("=" * 70)
    
    # Step 1: Check credentials
    print("\n[Step 1] Checking credentials...")
    check_credentials()
    
    # Step 2: Create function configuration
    print("\n[Step 2] Creating function configuration...")
    config = Config(
        provider="cloudflare",
        function_name="weather_api",
        timeout=30,
        environment={
            "ENV": "production",
            "VERSION": "1.0.0"
        }
    )
    print(f"  ✓ Function name: {config.function_name}")
    print(f"  ✓ Provider: {config.provider}")
    print(f"  ✓ Timeout: {config.timeout}s")
    
    # Step 3: Create Function instance
    print("\n[Step 3] Creating Function instance...")
    fn = Function(weather_api, config)
    print(f"  ✓ Function: {fn.metadata['name']}")
    print(f"  ✓ Source code extracted: {len(fn.metadata['source_code'])} chars")
    
    # Step 4: Deploy to Cloudflare
    print("\n[Step 4] Deploying to Cloudflare Workers...")
    print("  (This will make an API call to Cloudflare)")
    
    try:
        result = fn.deploy()
        
        print("\n" + "=" * 70)
        print("✅ DEPLOYMENT SUCCESSFUL!")
        print("=" * 70)
        print(f"\nFunction Details:")
        print(f"  Name: {result['function_name']}")
        print(f"  Provider: {result['provider']}")
        print(f"  URL: {result['url']}")
        print(f"\nYou can now invoke your function:")
        print(f"  curl -X POST {result['url']} \\")
        print(f"    -H 'Content-Type: application/json' \\")
        print(f"    -d '{{\"city\": \"San Francisco\"}}'")
        print(f"\nOr use the CLI:")
        print(f"  unified invoke {result['function_name']} --payload '{{\"city\": \"New York\"}}'")
        
        # Step 5: Test invocation
        print("\n[Step 5] Testing invocation...")
        test_payload = {"city": "San Francisco"}
        invoke_result = fn.invoke(test_payload)
        
        print("\n" + "=" * 70)
        print("✅ INVOCATION SUCCESSFUL!")
        print("=" * 70)
        print(f"\nRequest: {test_payload}")
        print(f"Response: {invoke_result}")
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ DEPLOYMENT FAILED")
        print("=" * 70)
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("  1. Verify your API token has Workers Scripts:Edit permission")
        print("  2. Check your Account ID is correct")
        print("  3. Ensure you have network connectivity")
        print("  4. Check Cloudflare dashboard for any issues")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("🎉 COMPLETE - Your function is live on Cloudflare Workers!")
    print("=" * 70)


if __name__ == "__main__":
    main()
