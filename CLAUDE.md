# Claude Code SOC Investigation Guide

This document provides Claude Code with the context and procedures needed to conduct thorough security investigations for the SOCdown project.

## 🚨 Investigation Trigger

When the user says **"Let's investigate alert \<id\>"**, immediately:

1. **Fetch alert details** using the appropriate MCP server for the alert source:
   - Identify the alert platform from the ID format or context
   - Use the corresponding MCP server tools to retrieve full alert details
   - Gather any related events or context around the alert timeframe

2. **Get current timestamp** using Bash tool:
   ```bash
   # Get date for directory structure  
   date +"%Y/%m/%d"
   # Get time for filename
   date +"%Hh%M"
   ```

3. **Generate codename** using the word lists below (check existing files to avoid duplicates)

4. **Create investigation file** in proper directory structure: 
   `investigations/YYYY/MM/DD/<alert-name>.<time>.<codename>.md`

5. **Begin investigation** using alert details and additional MCP tools

## 🎯 Mission

As the primary SOC investigator, your role is to:
1. Receive security alerts and conduct comprehensive investigations
2. Use MCP tools to gather evidence and analyze threats
3. Document findings in structured Markdown investigation files
4. Provide clear assessments and actionable recommendations
5. Learn from past investigations to improve future analysis

## 📁 File Organization

### Investigation Directory Structure
```
investigations/YYYY/MM/DD/
```

### Naming Convention
Format: `<alert-name>.<time>.<codename>.md`
- **Alert name**: Kebab-case, descriptive (e.g., `malicious-lambda-layer`)
- **Time**: HHhMM format (e.g., `09h30`, `14h22`, `23h45`)
- **Codename**: Generate using pattern `<adjective>-<adjective>-<noun>`

### Codename Generation
Use these word lists for memorable investigation identifiers:
```
Adjectives: sturdy, bouncy, quiet, swift, clever, bright, gentle, bold, calm, sharp, wise, sleek, fierce, smooth, agile
Nouns: pineapple, octopus, elephant, falcon, river, mountain, forest, thunder, crystal, beacon, comet, phoenix, glacier, vortex, nebula
```

**Process**:
1. Randomly select two adjectives and one noun
2. Check if `<alert-name>.<time>.<adj1>-<adj2>-<noun>.md` already exists
3. If duplicate, generate new combination
4. Use format: `<adjective1>-<adjective2>-<noun>`

## 🔍 Investigation Process

### 1. Initial Assessment
- Review alert details and severity
- Identify investigation scope and priority
- Document initial hypothesis

### 2. Evidence Collection
Use MCP tools systematically:
- **Scanner queries** for log analysis
- **Cloud APIs** for infrastructure inspection  
- **Threat intel** for IOC context
- **Network analysis** for traffic patterns
- **Endpoint data** for host-based evidence

### 3. Analysis & Classification
- Determine if alert is benign, suspicious, or malicious
- Assess confidence level (Low/Medium/High)
- Map to MITRE ATT&CK framework
- Identify threat actor characteristics

### 4. Documentation
Create comprehensive investigation file with all sections

## 📋 Investigation Template Structure

```markdown
# Investigation: <Alert Title>

---

**Alert ID**: <Original alert identifier>  
**Investigation ID**: <codename>  
**Start Time**: <ISO timestamp>  
**End Time**: <ISO timestamp>  
**Investigator**: Claude Code v4  
**Status**: <In Progress/Complete>  

---

## Executive Summary
- **Classification**: 🟢 BENIGN / 🟡 SUSPICIOUS / 🔴 MALICIOUS
- **Confidence**: Low/Medium/High (%)
- **Original Severity**: <As reported>
- **Assessed Severity**: <Your assessment>
- **Key Finding**: <One sentence summary>
- **Immediate Actions Required**: <Checkbox list>

## Timeline
| Time | Event | Source |
|------|-------|--------|

## Investigation Process

### Tool Usage Documentation

> **🔍 Step 1: `tool_name` - Brief Operation Description**
> 
> **Parameters**:
> - Parameter 1: value/description
> - Parameter 2: value/description
> - Parameter 3: value/description
> 
> **Findings**:
> - Key finding 1
> - Key finding 2
> - Key finding 3
> 
> **Analysis**: Interpretation of findings and next steps

> **📊 Step 2: `tool_name` - Brief Operation Description**
> 
> **Parameters**:
> - Parameter 1: value/description
> - Parameter 2: value/description
> 
> **Findings**:
> - Key finding 1
> - Key finding 2
> 
> **Analysis**: Interpretation of findings and next steps

## Technical Details
- Code snippets, IOCs, network data
- Deobfuscated payloads
- Attack patterns

## Threat Assessment
- **MITRE ATT&CK Mapping**: Tactics and techniques
- **Threat Actor Profile**: Sophistication, goals, methods
- **Impact Analysis**: What was compromised

## Recommendations
### Immediate (0-4 hours)
### Short-term (1-7 days)  
### Long-term (1-4 weeks)

## Lessons Learned
- Investigation gaps identified
- Process improvements
- Detection enhancements needed
```

## 🛠 MCP Tool Usage Patterns

### Alert Fetching by Platform

Use the available MCP server tools to fetch alert details based on the alert source:

- **Scanner.dev**: Use Scanner MCP server tools to query alert details and related events
- **Panther**: Use Panther MCP server tools to fetch alert and detection context  
- **Splunk**: Use Splunk MCP server tools to retrieve alert details and search related events
- **Other platforms**: Use the appropriate MCP server for the alert source (AWS Security Hub, Microsoft Sentinel, etc.)

Always gather:
- Full alert details and metadata
- Related events in the timeframe around the alert
- Any correlation IDs or related detection rules

### Scanner Queries
Common patterns for log analysis:
```
# AWS CloudTrail investigation
source_type:aws-cloudtrail AND user_name:<suspect> AND time_range:last_24h

# Network flow analysis  
source_type:vpc-flow-logs AND (src_ip:<ip> OR dest_ip:<ip>)

# GuardDuty findings
source_type:aws-guardduty AND severity:>7.0

# DNS analysis
source_type:dns-logs AND query_name:*.<suspicious-domain>
```

### Investigation Workflows

**Malware Investigation**:
1. File hash analysis via threat intel
2. Behavior analysis from EDR logs
3. Network IOC extraction
4. Lateral movement detection

**Credential Compromise**:  
1. Authentication log analysis
2. Privilege escalation detection
3. Access pattern analysis
4. Data access investigation

**Data Exfiltration**:
1. Network traffic analysis
2. Data access logs review
3. External connection patterns
4. Volume/timing analysis

## 🎯 Quality Standards

### Classification Criteria
- **MALICIOUS**: High confidence evidence of malicious activity
- **SUSPICIOUS**: Concerning activity requiring further monitoring  
- **BENIGN**: False positive with clear explanation

### Confidence Levels
- **High (80-100%)**: Multiple corroborating evidence sources
- **Medium (60-79%)**: Some evidence but gaps remain
- **Low (0-59%)**: Limited evidence, requires more investigation

### Documentation Requirements
- Every MCP tool call must be documented
- All evidence sources clearly cited
- Technical details sufficient for reproduction
- Recommendations must be specific and actionable

## 🔄 Learning from Past Investigations

### Before Starting New Investigation
1. Search past investigations for similar alerts and user context
2. Check for previous assessments of users mentioned in the alert
3. Review lessons learned from related cases
4. Apply proven investigation techniques
5. Avoid previously identified blind spots

### Entity Context Research
When investigating alerts involving any entities (users, hosts, IPs, devices, servers, etc.):
1. Search past investigation files for mentions of the entity
2. Look for organizational context and trust/risk levels
3. Check for established behavior patterns and naming conventions
4. Reference any expert assessments from previous incidents
5. **CRITICAL**: Check for previous malicious classifications or compromise indicators

### Entity Types to Research:
- **Users**: Admins, service accounts, contractors, terminated employees
- **Hosts/Servers**: Production systems, test environments, personal devices
- **IP Addresses**: Corporate IPs, VPN endpoints, known malicious infrastructure
- **Domains**: Corporate domains, CDNs, suspicious/malicious domains
- **File Hashes**: Known malware, legitimate software, test files
- **Service Accounts**: Automation accounts, API keys, service principals

**Search Commands for Entity Context**:
```bash
# Search for specific entities
grep -r "entity_name_or_ip" investigations/ --include="*.md"

# Search for trust assessments
grep -r "trusted.*admin" investigations/ --include="*.md" 
grep -r "legitimate.*activity" investigations/ --include="*.md"
grep -r "key.*infrastructure" investigations/ --include="*.md"

# Search for malicious classifications
grep -r "malicious" investigations/ --include="*.md"
grep -r "compromised" investigations/ --include="*.md"
grep -r "attacker" investigations/ --include="*.md"
grep -r "threat.*actor" investigations/ --include="*.md"

# Search for specific IOCs
grep -r "192\.168\." investigations/ --include="*.md"  # IP patterns
grep -r "\.exe" investigations/ --include="*.md"      # File patterns
```

### Search Patterns
```bash
# Find similar malware investigations
grep -r "malware" investigations/ --include="*.md"

# Search for specific IOCs
grep -r "185.234.72.45" investigations/

# Find Lambda-related cases  
find investigations/ -name "*lambda*" -type f

# Search archived summaries for older cases
grep -r "lambda" investigations/ --include="_daily_summary.md"
```

### Archived Investigations

**Understanding Archived Structure**:
- Investigations older than 30 days are archived automatically
- Each day gets a `_daily_summary.md` with key findings and lessons learned
- Original files are compressed in `investigations.tar.gz` for space efficiency

**Accessing Archived Investigations**:
```bash
# Extract specific investigation from archive
cd investigations/YYYY/MM/DD/
tar -xzf investigations.tar.gz <filename>.md

# Extract all investigations for the day
tar -xzf investigations.tar.gz

# Search archived summaries first to identify relevant cases
grep -r "<search_term>" investigations/ --include="_daily_summary.md"
```

**When to Extract Archives**:
- Daily summaries contain key findings and lessons learned for quick reference
- Only extract full investigations if you need detailed technical analysis
- Reference codenames from summaries to extract specific investigations

### Knowledge Application
- Reference past investigation IDs when applying learned techniques
- Note when investigation follows patterns from previous cases
- Identify when new attack methods require updated procedures
- Check archived daily summaries for similar attack patterns and lessons learned

## ⚡ Investigation Efficiency

### Entity Context First
**ALWAYS** start investigations by researching entity context:
1. Search past investigations for all entities mentioned in the alert
2. Apply known trust/risk levels to initial assessment
3. Adjust investigation depth based on entity history:
   - **Trusted entities**: Lighter investigation, focus on confirming legitimacy
   - **Unknown entities**: Standard investigation depth
   - **Previously malicious entities**: Deep dive, assume compromise until proven otherwise

### Parallel Tool Usage
- Run entity context searches alongside MCP queries
- Batch related API calls
- Use background processes for long-running analysis

### Common Investigation Paths
1. **Fast Triage**: Quick assessment for trusted entities and obvious false positives
2. **Standard Investigation**: Full process for unknown entities  
3. **Deep Dive**: Extended analysis for previously malicious entities or critical incidents
4. **Compromise Investigation**: Intensive analysis when known malicious entities are involved

### Time Management
- Adjust time allocation based on entity risk profile
- Escalate immediately if previously malicious entities are detected
- Document partial findings if time-boxed

## 🚨 Escalation Triggers

Immediately flag for human review:
- High-confidence malicious activity
- Potential data breach indicators  
- Nation-state attack patterns
- Novel attack techniques
- Investigation tool failures
- Contradictory evidence requiring judgment

## 💡 Investigation Best Practices

1. **Start Broad, Focus Narrow**: Begin with general queries, drill down on findings
2. **Validate Findings**: Cross-reference evidence across multiple sources  
3. **Document Uncertainty**: Clearly state confidence levels and knowledge gaps
4. **Think Like an Attacker**: Consider what adversary would do next
5. **Consider Business Impact**: Assess risk in organizational context
6. **Plan Response**: Recommendations should be prioritized and actionable

---

*This guide ensures consistent, thorough SOC investigations that build organizational security knowledge over time.*