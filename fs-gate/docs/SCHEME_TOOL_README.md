# Scheme Tool - Crop Damage Relief & Insurance Assistant

## Overview

The **Scheme Tool** is a comprehensive MCP (Model Context Protocol) tool designed to help farmers navigate crop damage situations by providing personalized guidance on:

- **Insurance Claims** (PMFBY, WBCIS, Private)
- **Government Relief Schemes** (SDRF, NDRF, State-specific)
- **Input Support Programs** (Seeds, Fertilizers, Equipment)
- **Recent Government Announcements** (Using EXA search)
- **Step-by-step Action Plans**
- **Document Checklists**
- **Contact Information**

## Key Features

### 🛡️ Insurance Guidance
- **PMFBY (Pradhan Mantri Fasal Bima Yojana)** claim process
- **WBCIS (Weather Based Crop Insurance)** automatic triggers
- **Private insurance** claim assistance
- Document requirements and timelines
- Helpline numbers and websites

### 🏛️ Government Relief Schemes
- **State Disaster Response Fund (SDRF)** applications
- **National Disaster Response Fund (NDRF)** for severe disasters
- **Kisan Credit Card** loan restructuring
- State-specific relief programs
- Eligibility criteria and application processes

### 🌱 Input Support Programs
- **Seed Subsidy Schemes** (50-75% subsidy)
- **Fertilizer Subsidies** through DBT
- **Equipment Support** for replanting
- **Soil Health Card** based recommendations

### 🔍 Real-time Relief Search
- **EXA Search Integration** for recent government announcements
- **PIB.gov.in** and **agricoop.gov.in** monitoring
- **State government** relief notifications
- **Disaster-specific** compensation updates

### 📋 Personalized Action Plans
- **Immediate Actions** (72-hour timeline)
- **Short-term Steps** (application processes)
- **Long-term Planning** (risk mitigation)
- **Document Preparation** checklists
- **Contact Information** for local officials

## API Usage

### HTTP Endpoint
```bash
POST /tools/scheme-tool
Content-Type: application/json

{
  "damage_type": "flood|drought|cyclone|hailstorm|pest_attack|disease|fire|unseasonal_rain|frost|other",
  "crop_type": "wheat|rice|cotton|sugarcane|maize|...",
  "state": "Punjab|Gujarat|Maharashtra|...",
  "district": "Ludhiana|Ahmedabad|Mumbai|...",
  "damage_extent": "minor|moderate|severe|complete",
  "has_insurance": true|false,
  "insurance_type": "pmfby|wbcis|private|none",
  "farmer_category": "small|marginal|medium|large",
  "land_size_acres": 5,
  "damage_date": "2024-10-28",
  "search_relief_schemes": true|false
}
```

### MCP Protocol
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "scheme-tool",
    "arguments": {
      "damage_type": "flood",
      "crop_type": "rice",
      "state": "Punjab",
      "district": "Ludhiana",
      "damage_extent": "severe",
      "has_insurance": true,
      "insurance_type": "pmfby",
      "land_size_acres": 5
    }
  }
}
```

## Response Structure

```json
{
  "success": true,
  "data": {
    "farmer_situation": {
      "damage_type": "flood",
      "crop_type": "rice",
      "location": { "state": "Punjab", "district": "Ludhiana" },
      "damage_extent": "severe",
      "has_insurance": true,
      "insurance_type": "pmfby",
      "land_size_acres": 5,
      "estimated_compensation": 50000
    },
    "recommendations": [
      {
        "category": "insurance_claim",
        "priority": "high",
        "action": "File Insurance Claim Immediately",
        "scheme": { /* PMFBY details */ },
        "steps": [ /* Claim process */ ],
        "documents": [ /* Required documents */ ],
        "timeline": "Report within 72 hours",
        "contact": "1800-200-7710"
      }
    ],
    "eligible_schemes": [ /* Government relief schemes */ ],
    "action_plan": {
      "immediate_actions": [ /* 72-hour tasks */ ],
      "short_term_actions": [ /* Application processes */ ],
      "long_term_actions": [ /* Future planning */ ]
    },
    "recent_relief_announcements": [ /* EXA search results */ ],
    "important_contacts": {
      "pmfby_helpline": "1800-200-7710",
      "kisan_call_center": "1800-180-1551",
      "district_collector": "Contact Ludhiana District Collector Office",
      "agriculture_officer": "Contact Ludhiana Agriculture Extension Officer"
    },
    "documents_checklist": [ /* Required documents */ ],
    "next_steps": [ /* Prioritized actions */ ]
  }
}
```

## Use Cases

### 1. Insured Farmer with Flood Damage
```bash
curl -X POST http://localhost:10001/tools/scheme-tool \
  -H "Content-Type: application/json" \
  -d '{
    "damage_type": "flood",
    "crop_type": "rice",
    "state": "Punjab",
    "district": "Ludhiana",
    "damage_extent": "severe",
    "has_insurance": true,
    "insurance_type": "pmfby",
    "land_size_acres": 5
  }'
```

**Result**: Immediate insurance claim guidance + SDRF application + input support schemes

### 2. Uninsured Farmer with Drought
```bash
curl -X POST http://localhost:10001/tools/scheme-tool \
  -H "Content-Type: application/json" \
  -d '{
    "damage_type": "drought",
    "crop_type": "wheat",
    "state": "Rajasthan",
    "district": "Jodhpur",
    "damage_extent": "complete",
    "has_insurance": false,
    "farmer_category": "small",
    "land_size_acres": 3
  }'
```

**Result**: Government relief schemes + insurance enrollment guidance + input support

### 3. Hailstorm Damage with Recent Relief Search
```bash
curl -X POST http://localhost:10001/tools/scheme-tool \
  -H "Content-Type: application/json" \
  -d '{
    "damage_type": "hailstorm",
    "crop_type": "cotton",
    "state": "Gujarat",
    "district": "Ahmedabad",
    "damage_extent": "moderate",
    "has_insurance": true,
    "search_relief_schemes": true
  }'
```

**Result**: Insurance claim + recent government announcements + local relief programs

## Integration with CropGPT Backend

The scheme-tool integrates seamlessly with the CropGPT backend through the MCP Gateway. When the AI detects crop damage or distress in farmer conversations, it automatically triggers the scheme-tool to provide relevant assistance.

### Trigger Conditions
- Keywords: "crop damage", "flood", "drought", "insurance", "compensation"
- Distress indicators: "crop failed", "heavy loss", "no harvest"
- Weather events: "cyclone hit", "hailstorm", "unseasonal rain"

### AI Integration Example
```javascript
// In the backend's agentic reasoning system
if (analysis.needs_scheme_assistance) {
  const schemeResult = await mcp.call_tool("scheme-tool", {
    damage_type: analysis.detected_damage_type,
    crop_type: analysis.crop_mentioned,
    state: user.location.state,
    district: user.location.district,
    has_insurance: analysis.insurance_mentioned,
    search_relief_schemes: true
  });
  
  // Provide personalized guidance based on farmer's situation
}
```

## Important Helplines

- **PMFBY Helpline**: 1800-200-7710
- **Kisan Call Center**: 1800-180-1551
- **National Helpline**: 1800-270-0224
- **Emergency**: Contact local District Collector

## Data Sources

- **Government Schemes Database**: PMFBY, SDRF, NDRF, State schemes
- **EXA Search**: Real-time government announcements
- **PIB.gov.in**: Press Information Bureau releases
- **agricoop.gov.in**: Ministry of Agriculture updates
- **State Government**: Relief notifications and updates

## Future Enhancements

1. **Real-time Weather Integration** - Automatic damage detection
2. **Satellite Imagery** - Crop damage assessment
3. **Mobile App Integration** - Photo-based damage reporting
4. **Blockchain Verification** - Transparent claim processing
5. **Multi-language Support** - Regional language assistance
6. **SMS/WhatsApp Integration** - Offline accessibility

## Contributing

To add new schemes or improve the tool:

1. Update the `schemeDatabase` in `schemeToolHandler`
2. Add new damage types to the enum
3. Enhance the EXA search queries
4. Test with various farmer scenarios
5. Update documentation

## License

This tool is part of the CropGPT Agricultural AI system and follows the same licensing terms.