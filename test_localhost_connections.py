#!/usr/bin/env python3
"""
Localhost Connection Test Script
Tests all components running on localhost for development
"""

import asyncio
import httpx
import json
import time
import subprocess
import sys
from typing import Dict, Any

# Test Configuration
MCP_SERVER_URL = "http://localhost:10000"
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

class LocalhostConnectionTest:
    """Test all localhost connections and integrations"""
    
    def __init__(self):
        self.test_results = []
        self.auth_token = None
        self.test_user_email = "test@localhost.com"
        self.test_user_password = "testpass123"
    
    async def run_all_tests(self):
        """Run complete localhost connection test suite"""
        print("🧪 Agricultural AI - Localhost Connection Test")
        print("=" * 60)
        
        # Test sequence
        tests = [
            ("🛠️ MCP Server Health", self.test_mcp_server_health),
            ("🔧 MCP Tools Availability", self.test_mcp_tools),
            ("🌾 Crop Price Tool", self.test_crop_price_tool),
            ("🔍 Search Tool", self.test_search_tool),
            ("🧪 Soil Health Tool", self.test_soil_health_tool),
            ("🌤️ Weather Tool", self.test_weather_tool),
            ("🐛 Pest Identifier Tool", self.test_pest_tool),
            ("💰 Mandi Price Tool", self.test_mandi_price_tool),
            ("🔧 Backend API Health", self.test_backend_health),
            ("👤 User Registration", self.test_user_registration),
            ("🔐 User Authentication", self.test_user_login),
            ("🤖 Backend-MCP Integration", self.test_backend_mcp_integration),
            ("🌐 Frontend Accessibility", self.test_frontend_access),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            try:
                print(f"\n{test_name}...")
                result = await test_func()
                if result:
                    print(f"   ✅ PASSED")
                    passed += 1
                else:
                    print(f"   ❌ FAILED")
                    failed += 1
                self.test_results.append({"test": test_name, "passed": result})
            except Exception as e:
                print(f"   ❌ ERROR: {e}")
                failed += 1
                self.test_results.append({"test": test_name, "passed": False, "error": str(e)})
        
        # Summary
        print(f"\n🎯 Test Summary:")
        print(f"   ✅ Passed: {passed}")
        print(f"   ❌ Failed: {failed}")
        print(f"   📊 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        if failed == 0:
            print(f"\n🏆 ALL TESTS PASSED! System is ready for development! 🚀")
        else:
            print(f"\n⚠️ Some tests failed. Check the issues above.")
            self.print_troubleshooting_guide()
        
        return failed == 0
    
    async def test_mcp_server_health(self) -> bool:
        """Test MCP server health"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{MCP_SERVER_URL}/health")
                if response.status_code == 200:
                    health_data = response.json()
                    print(f"      MCP Server Status: {health_data.get('status')}")
                    print(f"      Available Tools: {', '.join(health_data.get('tools', []))}")
                    return health_data.get("status") == "healthy"
                return False
        except Exception as e:
            print(f"      Error: {e}")
            return False
    
    async def test_mcp_tools(self) -> bool:
        """Test MCP tools availability"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{MCP_SERVER_URL}/")
                if response.status_code == 200:
                    data = response.json()
                    tools = data.get('tools', [])
                    print(f"      Found {len(tools)} tools")
                    for tool in tools[:3]:  # Show first 3 tools
                        print(f"        - {tool['name']}: {tool['description'][:50]}...")
                    return len(tools) >= 6  # Should have 6 tools
                return False
        except Exception as e:
            print(f"      Error: {e}")
            return False
    
    async def test_crop_price_tool(self) -> bool:
        """Test crop price tool directly"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    f"{MCP_SERVER_URL}/tools/crop-price",
                    json={
                        "state": "Punjab",
                        "commodity": "Wheat",
                        "limit": 5
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    success = data.get("success", False)
                    if success:
                        records = data.get("data", {}).get("records", [])
                        print(f"      Retrieved {len(records)} price records")
                    return success
                return False
        except Exception as e:
            print(f"      Error: {e}")
            return False
    
    async def test_search_tool(self) -> bool:
        """Test search tool directly"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    f"{MCP_SERVER_URL}/tools/search",
                    json={
                        "query": "Indian agriculture news 2024",
                        "num_results": 3
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    success = data.get("success", False)
                    if success:
                        results = data.get("data", {}).get("results", [])
                        print(f"      Retrieved {len(results)} search results")
                    return success
                return False
        except Exception as e:
            print(f"      Error: {e}")
            return False
    
    async def test_soil_health_tool(self) -> bool:
        """Test soil health tool directly"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    f"{MCP_SERVER_URL}/tools/soil-health",
                    json={
                        "state": "Punjab",
                        "ph_level": 6.5,
                        "npk_values": {
                            "nitrogen": 280,
                            "phosphorus": 23,
                            "potassium": 280
                        }
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    success = data.get("success", False)
                    if success:
                        analysis = data.get("data", {}).get("analysis", {})
                        health_score = analysis.get("health_score", 0)
                        print(f"      Soil Health Score: {health_score}/100")
                    return success
                return False
        except Exception as e:
            print(f"      Error: {e}")
            return False
    
    async def test_weather_tool(self) -> bool:
        """Test weather tool directly"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    f"{MCP_SERVER_URL}/tools/weather",
                    json={
                        "location": "Punjab, India",
                        "days": 7,
                        "include_farming_alerts": True
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    success = data.get("success", False)
                    if success:
                        forecast = data.get("data", {}).get("forecast", [])
                        alerts = data.get("data", {}).get("alerts", [])
                        print(f"      Weather forecast: {len(forecast)} days, {len(alerts)} alerts")
                    return success
                return False
        except Exception as e:
            print(f"      Error: {e}")
            return False
    
    async def test_pest_tool(self) -> bool:
        """Test pest identifier tool directly"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    f"{MCP_SERVER_URL}/tools/pest-identifier",
                    json={
                        "crop": "rice",
                        "symptoms": "yellowing leaves, stunted growth",
                        "location": "Punjab"
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    success = data.get("success", False)
                    if success:
                        analysis = data.get("data", {}).get("analysis", {})
                        identification = analysis.get("identification")
                        if identification:
                            print(f"      Identified: {identification.get('pest_name')} ({identification.get('confidence_score')}% confidence)")
                    return success
                return False
        except Exception as e:
            print(f"      Error: {e}")
            return False
    
    async def test_mandi_price_tool(self) -> bool:
        """Test mandi price tool directly"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    f"{MCP_SERVER_URL}/tools/mandi-price",
                    json={
                        "commodity": "wheat",
                        "state": "Punjab",
                        "district": "Ludhiana",
                        "include_predictions": True
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    success = data.get("success", False)
                    if success:
                        price_data = data.get("data", {})
                        current_price = price_data.get("current_price")
                        predictions = price_data.get("predictions", [])
                        print(f"      Current price: ₹{current_price}, {len(predictions)} predictions")
                    return success
                return False
        except Exception as e:
            print(f"      Error: {e}")
            return False
    
    async def test_backend_health(self) -> bool:
        """Test backend API health"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{BACKEND_URL}/api/health")
                if response.status_code == 200:
                    health_data = response.json()
                    print(f"      Backend Status: {health_data.get('status')}")
                    mcp_status = health_data.get('services', {}).get('mcp_gateway', 'unknown')
                    print(f"      MCP Gateway Connection: {mcp_status}")
                    return health_data.get("status") == "healthy"
                return False
        except Exception as e:
            print(f"      Error: {e}")
            return False
    
    async def test_user_registration(self) -> bool:
        """Test user registration"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{BACKEND_URL}/api/auth/register",
                    json={
                        "email": self.test_user_email,
                        "password": self.test_user_password
                    }
                )
                # 200/201 for success, 400 if user already exists
                return response.status_code in [200, 201, 400]
        except Exception as e:
            print(f"      Error: {e}")
            return False
    
    async def test_user_login(self) -> bool:
        """Test user authentication"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{BACKEND_URL}/api/auth/login",
                    json={
                        "email": self.test_user_email,
                        "password": self.test_user_password
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    self.auth_token = data.get("access_token")
                    print(f"      Login successful, token received")
                    return self.auth_token is not None
                return False
        except Exception as e:
            print(f"      Error: {e}")
            return False
    
    async def test_backend_mcp_integration(self) -> bool:
        """Test backend integration with MCP gateway"""
        if not self.auth_token:
            return False
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{BACKEND_URL}/api/chat",
                    json={"message": "What is the current price of wheat in Punjab?"},
                    headers={"Authorization": f"Bearer {self.auth_token}"}
                )
                if response.status_code == 200:
                    data = response.json()
                    tools_used = data.get("tools_used", [])
                    message = data.get("message", "")
                    print(f"      Tools used: {tools_used}")
                    print(f"      Response length: {len(message)} characters")
                    return len(message) > 50  # Should have a meaningful response
                return False
        except Exception as e:
            print(f"      Error: {e}")
            return False
    
    async def test_frontend_access(self) -> bool:
        """Test frontend accessibility"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(FRONTEND_URL)
                return response.status_code == 200
        except Exception as e:
            print(f"      Error: {e}")
            return False
    
    def print_troubleshooting_guide(self):
        """Print troubleshooting guide for failed tests"""
        print(f"\n🔧 Troubleshooting Guide:")
        print(f"")
        print(f"1. **MCP Server Issues:**")
        print(f"   - Make sure you're in the fs-gate directory")
        print(f"   - Run: npm install && npm run dev")
        print(f"   - Check port 10000 is available")
        print(f"")
        print(f"2. **Backend Issues:**")
        print(f"   - Make sure you're in the backend directory")
        print(f"   - Run: pip install -r requirements.txt")
        print(f"   - Run: uvicorn server:app --reload --port 8000")
        print(f"   - Check MongoDB is running (or use MongoDB Atlas)")
        print(f"")
        print(f"3. **Frontend Issues:**")
        print(f"   - Make sure you're in the frontend directory")
        print(f"   - Run: npm install --legacy-peer-deps")
        print(f"   - Run: npm start")
        print(f"   - Check port 3000 is available")
        print(f"")
        print(f"4. **API Keys:**")
        print(f"   - Check .env files have correct API keys")
        print(f"   - CEREBRAS_API_KEY, DATAGOVIN_API_KEY, EXA_API_KEY")
        print(f"")

async def main():
    """Run the localhost connection test"""
    tester = LocalhostConnectionTest()
    success = await tester.run_all_tests()
    
    if success:
        print("\n🎉 Localhost Connection Test: PASSED")
        print("🚀 Your Agricultural AI system is ready for development!")
        print("\n📋 Next Steps:")
        print("   1. Start MCP Server: cd fs-gate && npm run dev")
        print("   2. Start Backend: cd backend && uvicorn server:app --reload")
        print("   3. Start Frontend: cd frontend && npm start")
        print("   4. Open http://localhost:3000 in your browser")
    else:
        print("\n⚠️ Localhost Connection Test: FAILED")
        print("🔧 Please check the failed tests and fix issues before proceeding.")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())