#!/usr/bin/env node

/**
 * Test Script for Scheme Tool
 * Demonstrates various crop damage scenarios and scheme recommendations
 */

import fetch from 'node-fetch';

const BASE_URL = 'http://localhost:10000';

// Test scenarios
const testScenarios = [
  {
    name: "🌊 Flood Damage - Insured Rice Farmer",
    data: {
      damage_type: "flood",
      crop_type: "rice",
      state: "Punjab",
      district: "Ludhiana",
      damage_extent: "severe",
      has_insurance: true,
      insurance_type: "pmfby",
      land_size_acres: 5,
      farmer_category: "small",
      search_relief_schemes: true
    }
  },
  {
    name: "☀️ Drought - Uninsured Wheat Farmer",
    data: {
      damage_type: "drought",
      crop_type: "wheat",
      state: "Rajasthan",
      district: "Jodhpur",
      damage_extent: "complete",
      has_insurance: false,
      farmer_category: "marginal",
      land_size_acres: 2,
      search_relief_schemes: true
    }
  },
  {
    name: "🌨️ Hailstorm - Cotton Farmer with WBCIS",
    data: {
      damage_type: "hailstorm",
      crop_type: "cotton",
      state: "Gujarat",
      district: "Ahmedabad",
      damage_extent: "moderate",
      has_insurance: true,
      insurance_type: "wbcis",
      land_size_acres: 8,
      farmer_category: "medium",
      search_relief_schemes: true
    }
  },
  {
    name: "🐛 Pest Attack - Sugarcane Farmer",
    data: {
      damage_type: "pest_attack",
      crop_type: "sugarcane",
      state: "Maharashtra",
      district: "Pune",
      damage_extent: "severe",
      has_insurance: false,
      farmer_category: "large",
      land_size_acres: 15,
      search_relief_schemes: false
    }
  }
];

async function testSchemeToolHTTP(scenario) {
  try {
    console.log(`\n🧪 Testing: ${scenario.name}`);
    console.log('📊 Input:', JSON.stringify(scenario.data, null, 2));
    
    const response = await fetch(`${BASE_URL}/tools/scheme-tool`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(scenario.data)
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const result = await response.json();
    
    if (result.success) {
      console.log('✅ Success!');
      console.log(`💰 Estimated Compensation: ₹${result.data.farmer_situation.estimated_compensation}`);
      console.log(`📋 Recommendations: ${result.data.recommendations.length}`);
      console.log(`🏛️ Eligible Schemes: ${result.data.eligible_schemes.length}`);
      console.log(`📰 Recent Announcements: ${result.data.recent_relief_announcements.length}`);
      
      // Show top recommendation
      if (result.data.recommendations.length > 0) {
        const topRec = result.data.recommendations[0];
        console.log(`🎯 Top Recommendation: ${topRec.action} (${topRec.priority} priority)`);
      }
      
      // Show immediate actions
      if (result.data.action_plan.immediate_actions.length > 0) {
        console.log('⚡ Immediate Actions:');
        result.data.action_plan.immediate_actions.forEach((action, i) => {
          console.log(`   ${i + 1}. ${action}`);
        });
      }
    } else {
      console.log('❌ Failed:', result.error);
    }
    
  } catch (error) {
    console.log('❌ Error:', error.message);
  }
}

async function testSchemeToolMCP(scenario) {
  try {
    console.log(`\n🔌 Testing MCP: ${scenario.name}`);
    
    const mcpRequest = {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: {
        name: "scheme-tool",
        arguments: scenario.data
      }
    };
    
    const response = await fetch(`${BASE_URL}/mcp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(mcpRequest)
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const result = await response.json();
    
    if (result.result && result.result.content) {
      console.log('✅ MCP Success!');
      const data = JSON.parse(result.result.content[0].text);
      console.log(`💰 Estimated Compensation: ₹${data.farmer_situation.estimated_compensation}`);
      console.log(`📋 Recommendations: ${data.recommendations.length}`);
    } else if (result.error) {
      console.log('❌ MCP Error:', result.error.message);
    }
    
  } catch (error) {
    console.log('❌ MCP Error:', error.message);
  }
}

async function checkServerHealth() {
  try {
    console.log('🏥 Checking server health...');
    const response = await fetch(`${BASE_URL}/health`);
    const health = await response.json();
    
    if (health.status === 'healthy') {
      console.log('✅ Server is healthy');
      console.log(`🛠️ Available tools: ${health.tools.join(', ')}`);
      return true;
    } else {
      console.log('❌ Server is not healthy');
      return false;
    }
  } catch (error) {
    console.log('❌ Cannot connect to server:', error.message);
    console.log('💡 Make sure to start the server with: npm start');
    return false;
  }
}

async function runTests() {
  console.log('🚀 Scheme Tool Test Suite');
  console.log('=' .repeat(50));
  
  // Check server health first
  const isHealthy = await checkServerHealth();
  if (!isHealthy) {
    process.exit(1);
  }
  
  console.log('\n📡 Testing HTTP Endpoints');
  console.log('-'.repeat(30));
  
  // Test HTTP endpoints
  for (const scenario of testScenarios) {
    await testSchemeToolHTTP(scenario);
    await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second between tests
  }
  
  console.log('\n🔌 Testing MCP Protocol');
  console.log('-'.repeat(30));
  
  // Test MCP protocol (just first scenario to avoid spam)
  await testSchemeToolMCP(testScenarios[0]);
  
  console.log('\n✨ Test Suite Complete!');
  console.log('=' .repeat(50));
  console.log('💡 The scheme-tool is ready for integration with CropGPT backend');
  console.log('🔗 Use the MCP Gateway to connect this tool to your AI system');
}

// Run tests if this script is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  runTests().catch(console.error);
}

export { testSchemeToolHTTP, testSchemeToolMCP, checkServerHealth };