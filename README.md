# SOCdown

**SOC + Markdown = SOCdown**

The simplest possible approach to security operations: every alert investigation
becomes a version-controlled Markdown artifact, harnessing the mystical powers
of the format that AIs understand better than humans. Instead of alerts
disappearing into SIEM logs, each investigation is conducted by Claude Code
and/or human analysts using MCP tools and documented as a comprehensive 
Markdown file that can be reviewed, refined, and learned from.

## 🎯 Core Concept

Transform SOC operations into a knowledge base where:
- **Claude Code** conducts autonomous investigations using MCP security tools
- **Each alert** gets its own detailed Markdown investigation file  
- **Human analysts** can review and iterate as needed, or Claude can open PRs directly
- **Past investigations** become searchable knowledge for future cases
- **Investigation quality** improves over time through documented lessons learned

## 📁 Repository Structure

```
socdown/
├── investigations/           # All security investigations
│   └── YYYY/MM/DD/          # Date-partitioned structure
│       ├── alert-name.HHhMM.codename.md
│       └── ...
├── templates/               # Investigation templates
├── tools/                   # MCP tool configurations
└── docs/                    # Additional documentation
```

## 📝 Investigation Naming Convention

Format: `<alert-name>.<time>.<codename>.md`

Examples:
- `malicious-lambda-layer.09h30.sturdy-playful-pineapple.md`
- `suspicious-rdp-login.14h22.bouncy-clever-octopus.md` 
- `data-exfil-attempt.23h45.quiet-swift-elephant.md`

**Components**:
- **Alert name**: Kebab-case description of the security event
- **Time**: Investigation start time in HHhMM format
- **Codename**: Three random playful words for memorable reference
- **Date**: Implicit from directory structure (YYYY/MM/DD)

## 🔍 Investigation Workflow

1. **Alert Triggered** → Security tool generates alert
2. **Claude Investigates** → Uses MCP tools to gather evidence and analyze
3. **Documentation Created** → Comprehensive Markdown file generated
4. **Autonomous or Human Review** → Claude can commit directly or open PR for human review
5. **Investigation Finalized** → Approved investigation becomes permanent record
6. **Knowledge Accumulated** → Future investigations reference past cases

## 📋 Investigation Structure

Each investigation includes:

- **Executive Summary**: Classification, confidence, severity assessment
- **Timeline**: Chronological sequence of security events
- **Investigation Process**: Detailed tool usage and findings
- **Technical Analysis**: IOCs, attack patterns, technical details  
- **Threat Assessment**: MITRE ATT&CK mapping and threat actor profiling
- **Recommendations**: Immediate, short-term, and long-term actions
- **Lessons Learned**: Insights for improving future investigations

## 🛠 MCP Tool Integration

SOCdown leverages MCP (Model Context Protocol) tools for security investigations:

- **SIEM Queries**: Search logs across security platforms
- **Threat Intelligence**: IOC lookups and threat context
- **Cloud APIs**: AWS, Azure, GCP security analysis
- **Network Analysis**: Flow logs, DNS queries, traffic analysis
- **Endpoint Data**: EDR queries, process analysis, file inspection
- **Vulnerability Assessment**: CVE lookups, patch status

## 🎯 Key Benefits

**For SOC Teams**:
- Scale investigation capacity without hiring more analysts
- Maintain detailed documentation of every alert
- Learn from past investigations to improve response
- Human analysts focus on complex cases, Claude handles routine investigations

**For Organizations**:
- Complete audit trail of all security investigations  
- Consistent investigation quality and methodology
- Knowledge retention when team members leave
- Faster mean time to resolution (MTTR)

**For Compliance**:
- Detailed evidence chain for incident response
- Documented decision-making process
- Historical investigation records
- Consistent reporting format

## 🚀 Getting Started

1. **Setup MCP Tools**: Configure security tool connections
2. **Create Investigation**: Claude conducts alert investigation
3. **Autonomous or Manual Review**: Claude commits directly or opens PR for human review
4. **Document Lessons**: Add insights for future reference
5. **Iterate**: Continuously improve investigation quality

## 🔄 Investigation Lifecycle

```
Alert → Investigate → Document → Review → Approve → Learn → Repeat
```

Each cycle improves the overall SOC capability by adding to the collective knowledge base.

## 🎓 Philosophy

> "What if every security investigation became as reviewable, searchable, and improvable as code?"

SOCdown treats security investigations like software development:
- Version controlled artifacts
- Peer review process  
- Continuous improvement
- Knowledge sharing
- Documented decision-making

---

*Transform your SOC from reactive alert processing to proactive knowledge building.*
