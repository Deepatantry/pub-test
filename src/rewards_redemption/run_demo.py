#!/usr/bin/env python3
"""
Rewards & Redemption System Demo Runner

This script provides multiple ways to run and test the system:
1. CLI Demo - Interactive command-line interface
2. Web API - FastAPI server with REST endpoints
3. Web UI - HTML interface for browser-based testing
"""

import asyncio
import sys
import subprocess
import os
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("🏆 REWARDS & REDEMPTION SYSTEM DEMO")
    print("=" * 60)
    print("Choose your demo experience:")
    print("1. CLI Demo - Interactive command-line interface")
    print("2. Web API - Start FastAPI server (localhost:8000)")
    print("3. Web UI - Open browser demo interface")
    print("4. Run Tests - Execute integration tests")
    print("5. Exit")
    print("=" * 60)

async def run_cli_demo():
    print("\n🚀 Starting CLI Demo...")
    from demo.cli_demo import main
    await main()

def run_web_api():
    print("\n🌐 Starting Web API Server...")
    print("Server will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Demo UI: http://localhost:8000")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        import uvicorn
        from app import app
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

def run_web_ui():
    print("\n🖥️  Starting Web UI...")
    print("This will start the API server and open the demo interface")
    
    # Start server in background
    import threading
    import time
    import webbrowser
    
    def start_server():
        import uvicorn
        from app import app
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(3)
    
    # Open browser
    webbrowser.open("http://localhost:8000")
    print("Demo interface opened in browser")
    print("Press Enter to stop...")
    input()

def run_tests():
    print("\n🧪 Running Integration Tests...")
    
    # Simple test runner
    async def test_system():
        from demo.cli_demo import RewardsRedemptionDemo
        
        demo = RewardsRedemptionDemo()
        
        print("✓ System initialization")
        
        # Test categories
        categories = demo.category_service.get_active_categories()
        assert len(categories) > 0, "No active categories found"
        print("✓ Category management")
        
        # Test insights
        insights = demo.insights_service.generate_insights("member1")
        assert insights["member_id"] == "member1", "Insights generation failed"
        print("✓ Spending insights")
        
        # Test catalog
        catalog = demo.catalog_service.get_catalog()
        assert len(catalog["items"]) > 0, "No catalog items found"
        print("✓ Redemption catalog")
        
        # Test redemption
        result = demo.redemption_service.process_manual_redemption("member1", "redeem_1")
        assert result["success"], f"Redemption failed: {result.get('error')}"
        print("✓ Manual redemption")
        
        # Test value analysis
        analysis = demo.value_service.get_best_value_recommendations(limit=3)
        assert len(analysis) > 0, "No value recommendations found"
        print("✓ Value optimization")
        
        print("\n🎉 All tests passed!")
    
    asyncio.run(test_system())

def main():
    while True:
        print_banner()
        
        try:
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == "1":
                asyncio.run(run_cli_demo())
            elif choice == "2":
                run_web_api()
            elif choice == "3":
                run_web_ui()
            elif choice == "4":
                run_tests()
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid option. Please try again.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()