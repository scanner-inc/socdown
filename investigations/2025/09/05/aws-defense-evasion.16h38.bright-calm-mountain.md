# Investigation: AWS CloudTrail Defense Evasion Alert

---

**Alert ID**: bc93ebaa-4ae5-41ef-bdd1-108c692e4b0b  
**Investigation ID**: bright-calm-mountain  
**Start Time**: 2025-09-05T21:38:00Z  
**End Time**: 2025-09-05T21:40:00Z  
**Investigator**: Claude Code v4  
**Status**: Complete  

---

## Executive Summary
- **Classification**: 🟢 BENIGN
- **Confidence**: High (100%) - **Updated by Cliff Crosland**
- **Original Severity**: Low
- **Assessed Severity**: Informational
- **Key Finding**: User "leo" (confirmed key infrastructure admin) deleted test CloudWatch alarm "leo-test-usw2" - legitimate test resource cleanup activity
- **Immediate Actions Required**: 
  - [x] **RESOLVED**: Leo confirmed as trusted key infrastructure admin 
  - [ ] Consider adding Leo to admin exception list when Scanner supports lookup tables
  - [ ] Review detection rule tuning for trusted admin activities

## Timeline
| Time | Event | Source |
|------|-------|--------|
| 2025-08-09T05:05:37Z | Defense evasion alert triggered | Scanner Detection Engine |
| 2025-08-09T04:56:00Z to 2025-08-09T04:57:00Z | Detection time window | Alert Metadata |

## Investigation Process

### Tool Usage Documentation

> **🔍 Step 1: `mcp__scanner__execute_query` - Alert Lookup**
> 
> **Parameters**:
> - Query: `@index="_detections" id:"bc93ebaa-4ae5-41ef-bdd1-108c692e4b0b"`
> - Time Range: 1970-01-01 to 2025-12-31 (wide range for alert lookup)
> 
> **Findings**:
> - Alert found in detections index
> - Rule name: "AWS CloudTrail - Defense evasion through deletion of security measures"
> - Detection rule ID: 81a04b2f-c232-417d-9d9c-f1968e4c145d
> - MITRE ATT&CK: TA0005 (Defense Evasion), T1529 (System Shutdown/Reboot)
> - Matched 1 CloudTrail event showing security measure deletion
> 
> **Analysis**: This is a legitimate security detection rule targeting AWS defense evasion - significantly different from the test webhook rule, indicating a potentially serious security event

> **📋 Step 2: `mcp__scanner__fetch_cached_results` - Detection Rule Analysis**
> 
> **Parameters**:
> - Result handle: 7a2bffec-6a36-4e8b-af2e-b785e3083a0c
> - Fields: query_text, name, description, tags
> 
> **Findings**:
> - Full detection query retrieved
> - Targets specific AWS security deletion events (DeleteAlarms, DeleteDetector, DeleteIPSet, etc.)
> - Excludes legitimate scnr-deployer actions
> 
> **Analysis**: This is a well-crafted detection rule that filters out known legitimate automation while catching potential malicious deletions - the alert warrants investigation

> **🚨 Step 3: `mcp__scanner__execute_query` - Triggering Event Analysis**
> 
> **Parameters**:
> - Query: Full detection rule query for the alert timeframe
> - Time Range: 2025-08-09T04:56:00Z to 2025-08-09T04:57:00Z
> 
> **Findings**:
> - User "leo" executed DeleteAlarms API call targeting CloudWatch alarm "leo-test-usw2"
> - MFA authenticated session (true)
> - Source IP: 157.131.160.92
> - User Agent: AWS Internal
> - Account: 152394329118 (us-west-2 region)
> - User ARN: arn:aws:iam::152394329118:user/leo
> - Session Creation: 2025-08-08T17:43:38Z
> 
> **Analysis**: The deletion was performed by Leo (confirmed key infrastructure admin) with proper MFA authentication. The alarm name "leo-test-usw2" clearly indicates test resource cleanup activity - legitimate administrative action

> **🔍 Step 4: `mcp__scanner__execute_query` - IP Address Investigation**
> 
> **Parameters**:
> - Query: IOC search for IP address 157.131.160.92
> - Time Range: Extended period around alert
> 
> **Findings**:
> - IP associated with both user "leo" and scnr-deployer activities
> - 10 events from same IP showing legitimate AWS console usage
> - Mixed activity: user "leo" (2 events) and scnr-deployer role (8 events)
> - All events show successful operations with MFA authentication
> 
> **Analysis**: The source IP shows legitimate usage patterns with both user and automated activities, suggesting a corporate/VPN IP rather than malicious infrastructure. This supports the legitimacy hypothesis but doesn't eliminate the need for user verification

## Technical Details

### Alert Metadata
- **Alert ID**: bc93ebaa-4ae5-41ef-bdd1-108c692e4b0b
- **Detection Rule ID**: 81a04b2f-c232-417d-9d9c-f1968e4c145d
- **Rule Name**: AWS CloudTrail - Defense evasion through deletion of security measures
- **Description**: An attacker could evade defenses by deleting logs, alarms, detectors, rules, and other security measures
- **Severity**: Low (ID: 2) - **UNDERASSESSED**
- **Results**: 1 matching CloudTrail event
- **Time Range**: 2025-08-09T04:56:00Z to 2025-08-09T04:57:00Z
- **Alert Generated**: 2025-08-09T05:05:37Z

### Detection Query Analysis
```
%ingest.source_type: "aws:cloudtrail"
and eventName:(DeleteAlarms or DeleteDetector or DeleteIPSet or DeleteLogStream or DeleteLoggingConfiguration or DeleteRule or DeleteRuleGroup or DeleteWebACL)
and not userIdentity.sessionContext.sessionIssuer.userName: "scnr-deployer"
| count | where @q.count > 0
```

**Query Breakdown**:
- **Source**: AWS CloudTrail events
- **Target Events**: Security-related deletion operations:
  - DeleteAlarms (CloudWatch alarms)
  - DeleteDetector (GuardDuty detectors)
  - DeleteIPSet (WAF IP sets)
  - DeleteLogStream (CloudWatch log streams)
  - DeleteLoggingConfiguration (Various logging configs)
  - DeleteRule/DeleteRuleGroup (WAF/Config rules)
  - DeleteWebACL (Web Access Control Lists)
- **Exclusions**: Legitimate scnr-deployer service account actions
- **Logic**: Triggers on any occurrence of these deletion events

### MITRE ATT&CK Mapping
- **Primary Tactic**: TA0005 - Defense Evasion
- **Primary Technique**: T1529 - System Shutdown/Reboot
- **Additional Context**: Deleting security measures to avoid detection

## Threat Assessment

### MITRE ATT&CK Mapping
- **Tactic**: TA0005 - Defense Evasion
- **Technique**: T1529 - System Shutdown/Reboot
- **Sub-technique**: Disabling security tools and logging

### Evidence Analysis

**Core Event Details**:
- **Event**: AWS CloudWatch DeleteAlarms API call  
- **User**: leo (IAM user in account 152394329118)
- **Target**: CloudWatch alarm named "leo-test-usw2"
- **Timestamp**: 2025-08-09T04:56:55Z
- **Source IP**: 157.131.160.92
- **MFA Status**: Authenticated with MFA
- **User Agent**: AWS Internal (legitimate AWS console activity)
- **Request ID**: 1929ac47-cbfe-4ed5-a93d-65f3b7317384

**Session Context**:
- **Session Start**: 2025-08-08T17:43:38Z (long-lived session ~11 hours)
- **Principal ID**: AIDASG63I5QPE6UHNM6NF
- **Access Key**: ASIASG63I5QPBG2LGCBE (temporary credentials)
- **Console Session**: sessionCredentialFromConsole: true

**IP Address Analysis**:
- **157.131.160.92** appears in multiple legitimate activities
- Associated with both "leo" user and scnr-deployer role operations
- Pattern suggests shared corporate/office IP or VPN endpoint
- All operations from this IP show proper MFA authentication

**Behavioral Assessment**:
- Alarm name "leo-test-usw2" suggests test/development activity
- No follow-up malicious activity detected from user or IP
- Long session duration (11+ hours) typical of development work
- Mixed legitimate activities from same IP address

### Administrative Assessment (Updated by Cliff Crosland)
- **User Identity**: Leo - confirmed key infrastructure administrator with elevated privileges
- **Action Legitimacy**: Test resource cleanup activity - alarm name pattern "leo-test-usw2" clearly indicates personal testing
- **Security Posture**: Leo is trusted admin but requires monitoring due to high privilege level
- **Administrative Context**: Normal infrastructure maintenance activity

### Impact Analysis
- **Data Compromised**: None - legitimate administrative action
- **Systems Affected**: Test CloudWatch alarm "leo-test-usw2" (personal test resource)
- **Business Impact**: **NONE** - Authorized test resource cleanup by infrastructure admin

## Recommendations

### Immediate (0-4 hours)
- [x] **RESOLVED**: Investigation confirmed legitimate admin activity by Leo
- [ ] No further immediate action required for this specific event

### Short-term (1-7 days)  
- [ ] **False Positive Reduction**: Consider detection rule tuning for trusted admins
- [ ] Document Leo as key infrastructure admin in security procedures
- [ ] Review other defense evasion alerts for similar false positive patterns

### Long-term (1-4 weeks)
- [ ] **Enhancement Opportunity**: When Scanner supports lookup tables, add Leo to trusted admin exception list
- [ ] Implement tiered alerting - different severity for known admins vs unknown users  
- [ ] Create admin activity baselines to distinguish normal vs anomalous admin behavior
- [ ] Consider implementing admin action approval workflows for critical security deletions (non-test resources)

## Lessons Learned

### Investigation Gaps Identified (Resolved by Cliff Crosland Input)
- **Initial Gap**: Lacked organizational context about user "leo" being a trusted key infrastructure admin
- **Resolution**: Expert knowledge confirmed Leo's administrative role and legitimacy of test resource cleanup
- **Key Learning**: Need better user context database for investigations

### Process Improvements  
- **Admin Context Database**: Maintain updated list of key infrastructure admins for investigation reference
- **Test Resource Patterns**: Alarm names with user prefixes (e.g., "leo-test-*") likely indicate personal testing
- **Expert Consultation**: Leverage organizational knowledge when investigating admin activities

### Detection Enhancements Needed
- **Trusted Admin Exception Lists**: Implement lookup tables for known infrastructure admins when Scanner supports it
- **Tiered Alert Severity**: Different severity levels for known admins vs unknown users
- **Test Resource Recognition**: Pattern matching for test/development resource naming conventions
- **Admin Activity Baselines**: Establish normal behavior patterns for key admins to detect true anomalies