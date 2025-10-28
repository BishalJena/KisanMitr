# Scheme Tool Integration Guide for CropGPT Backend

## Overview

This guide explains how to integrate the **scheme-tool** with the CropGPT backend to automatically help farmers with crop damage situations.

## Backend Integration

### 1. Update the Agentic Reasoning System

In `backend/server.py`, modify the `analyze_task` method to detect crop damage scenarios:

```python
async def analyze_task(self, user_message: str) -> Dict[str, Any]:
    """Enhanced task analysis with scheme-tool detection"""
    
    # Existing analysis logic...
    
    # Add scheme-tool detection
    damage_keywords = [
        "crop damage", "flood", "drought", "cyclone", "hailstorm", 
        "pest attack", "disease", "fire", "crop failed", "heavy loss",
        "no harvest", "insurance", "compensation", "relief", "scheme"
    ]
    
    needs_scheme_assistance = any(keyword in user_message.lower() for keyword in damage_keywords)
    
    # Extract damage details using LLM
    if needs_scheme_assistance:
        damage_analysis = await self.extract_damage_details(user_message)
        analysis["needs_scheme_tool"] = True
        analysis["damage_details"] = damage_analysis
    
    return analysis
```

### 2. Add Damage Detail Extraction

```python
async def extract_damage_details(self, user_message: str) -> Dict[str, Any]:
    """Extract crop damage details from user message"""
    
    system_prompt = """Extract crop damage information from the farmer's message.
    
    Return JSON with:
    {
        "damage_type": "flood|drought|cyclone|hailstorm|pest_attack|disease|fire|other",
        "crop_type": "wheat|rice|cotton|...",
        "damage_extent": "minor|moderate|severe|complete",
        "has_insurance": true|false,
        "insurance_mentioned": "pmfby|wbcis|private|none",
        "location_mentioned": "state/district if mentioned"
    }
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    response = await self.cerebras.generate_response(messages)
    
    try:
        return json.loads(response)
    except:
        return {"damage_type": "other", "needs_manual_assessment": True}
```

### 3. Execute Scheme Tool

```python
async def execute_tools(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Enhanced tool execution with scheme-tool"""
    
    # Existing tool execution...
    
    # Execute scheme tool if needed
    if analysis.get("needs_scheme_tool") and analysis.get("damage_details"):
        damage_details = analysis["damage_details"]
        
        # Get user location from profile or ask
        user_location = await self.get_user_location(analysis.get("user_id"))
        
        scheme_params = {
            "damage_type": damage_details.get("damage_type", "other"),
            "crop_type": damage_details.get("crop_type"),
            "state": user_location.get("state"),
            "district": user_location.get("district"),
            "damage_extent": damage_details.get("damage_extent", "moderate"),
            "has_insurance": damage_details.get("has_insurance", False),
            "insurance_type": damage_details.get("insurance_mentioned", "none"),
            "search_relief_schemes": True
        }
        
        logger.info(f"Calling scheme-tool with params: {scheme_params}")
        result = await self.mcp.call_tool("scheme-tool", scheme_params)
        
        if result and not result.get("error"):
            tool_results["scheme_tool"] = result
            tools_used.append("scheme-tool")
            logger.info("Scheme-tool provided assistance")
    
    return {"tool_results": tool_results, "tools_used": tools_used}
```

### 4. Format Scheme Tool Response

```python
def format_scheme_response(self, scheme_data: Dict[str, Any], language: str = "en") -> str:
    """Format scheme tool response for farmer"""
    
    if not scheme_data or scheme_data.get("error"):
        return "I'm sorry, I couldn't retrieve scheme information right now. Please contact your local agriculture officer."
    
    data = scheme_data.get("data", {})
    farmer_situation = data.get("farmer_situation", {})
    recommendations = data.get("recommendations", [])
    
    response = f"""🚨 **Crop Damage Assistance**

**Your Situation:**
- Damage Type: {farmer_situation.get('damage_type', 'Unknown')}
- Crop: {farmer_situation.get('crop_type', 'Not specified')}
- Location: {farmer_situation.get('location', {}).get('district', 'Unknown')}, {farmer_situation.get('location', {}).get('state', 'Unknown')}
- Damage Extent: {farmer_situation.get('damage_extent', 'Unknown')}
- Estimated Compensation: ₹{farmer_situation.get('estimated_compensation', 0):,}

**🎯 Immediate Actions Required:**
"""
    
    # Add immediate actions
    immediate_actions = data.get("action_plan", {}).get("immediate_actions", [])
    for i, action in enumerate(immediate_actions[:3], 1):
        response += f"{i}. {action}\n"
    
    # Add top recommendations
    if recommendations:
        response += f"\n**📋 Top Recommendations:**\n"
        for rec in recommendations[:2]:
            response += f"• **{rec['action']}** ({rec['priority']} priority)\n"
            if rec.get('contact'):
                response += f"  📞 Contact: {rec['contact']}\n"
    
    # Add important contacts
    contacts = data.get("important_contacts", {})
    if contacts:
        response += f"\n**📞 Important Helplines:**\n"
        response += f"• PMFBY: {contacts.get('pmfby_helpline', 'N/A')}\n"
        response += f"• Kisan Call Center: {contacts.get('kisan_call_center', 'N/A')}\n"
    
    # Add recent relief announcements if available
    announcements = data.get("recent_relief_announcements", [])
    if announcements:
        response += f"\n**📰 Recent Government Relief:**\n"
        for announcement in announcements[:2]:
            response += f"• {announcement.get('title', 'Relief Announcement')}\n"
    
    response += f"\n💡 **Need more help?** I can provide detailed guidance on any specific scheme or process."
    
    return response
```

### 5. Update MCP Gateway Configuration

Ensure the scheme-tool is available in your MCP Gateway configuration:

```python
# In backend/server.py - MCPGatewayClient class
async def call_scheme_tool(self, damage_type: str, crop_type: str, state: str, district: str, **kwargs) -> Dict[str, Any]:
    """Call scheme-tool for crop damage assistance"""
    arguments = {
        "damage_type": damage_type,
        "crop_type": crop_type,
        "state": state,
        "district": district,
        **kwargs
    }
    
    result = await self._call_mcp_tool("scheme-tool", arguments)
    
    if "error" in result:
        return {"error": result["error"], "data": None}
    else:
        return {"data": result.get("data", result), "error": None}
```

## Frontend Integration

### 1. Add Scheme Assistance UI

In `frontend/src/components/ChatInterface.js`, add visual indicators for scheme assistance:

```javascript
// In the message rendering section
{message.tools_used && message.tools_used.includes('scheme-tool') && (
  <div className="scheme-assistance-badge">
    <span className="tool-badge scheme-badge">
      🛡️ Crop Damage Assistance
    </span>
  </div>
)}
```

### 2. Add Quick Action Buttons

```javascript
// Add quick action buttons for scheme-related responses
{message.scheme_data && (
  <div className="scheme-quick-actions">
    <button 
      className="quick-action-btn"
      onClick={() => handleExampleClick('Help me file insurance claim')}
    >
      📋 File Insurance Claim
    </button>
    <button 
      className="quick-action-btn"
      onClick={() => handleExampleClick('Show me government relief schemes')}
    >
      🏛️ Government Relief
    </button>
    <button 
      className="quick-action-btn"
      onClick={() => handleExampleClick('What documents do I need?')}
    >
      📄 Required Documents
    </button>
  </div>
)}
```

## Testing the Integration

### 1. Start the Scheme Tool Server

```bash
cd fs-gate
npm run build
npm start
```

### 2. Test with Sample Messages

Try these messages in the CropGPT chat:

- "My rice crop is damaged due to flood in Punjab"
- "Drought has destroyed my wheat crop, I have PMFBY insurance"
- "Hailstorm damaged my cotton crop yesterday, what should I do?"
- "My crops failed due to pest attack, need compensation"

### 3. Verify Tool Integration

Check that the backend:
1. Detects crop damage scenarios
2. Calls the scheme-tool with correct parameters
3. Formats the response appropriately
4. Provides actionable guidance

## Monitoring and Logging

Add logging to track scheme-tool usage:

```python
# In backend/server.py
logger.info(f"Scheme-tool triggered for user {user_id}: {damage_type} damage to {crop_type}")
logger.info(f"Scheme-tool recommendations: {len(recommendations)} provided")
logger.info(f"Estimated compensation: ₹{estimated_compensation}")
```

## Error Handling

```python
try:
    scheme_result = await self.mcp.call_scheme_tool(
        damage_type=damage_details["damage_type"],
        crop_type=damage_details.get("crop_type"),
        state=user_location["state"],
        district=user_location["district"]
    )
except Exception as e:
    logger.error(f"Scheme-tool error: {e}")
    # Fallback to basic guidance
    return "I understand you're facing crop damage. Please contact your local agriculture officer or call the Kisan helpline at 1800-180-1551 for immediate assistance."
```

## Performance Optimization

1. **Cache scheme data** for common scenarios
2. **Batch EXA searches** for multiple farmers in same region
3. **Pre-load relief announcements** during disaster seasons
4. **Use async processing** for non-critical searches

## Security Considerations

1. **Validate user location** before providing specific schemes
2. **Rate limit** scheme-tool calls to prevent abuse
3. **Sanitize inputs** to prevent injection attacks
4. **Log access** for audit purposes

This integration will make CropGPT a comprehensive crop damage assistance platform, automatically helping farmers navigate complex insurance and relief processes during their most challenging times.