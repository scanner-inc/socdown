#!/usr/bin/env python3
"""
SOCdown Investigation Archival Tool

Archives investigations older than X days by:
1. Creating a daily summary markdown file with key findings
2. Compressing original investigation files to save space
3. Maintaining searchable summaries for Claude to reference

Usage:
    python archive_investigations.py --days 30
    python archive_investigations.py --days 7 --dry-run
"""

import os
import sys
import gzip
import tarfile
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
import re

class InvestigationArchiver:
    def __init__(self, base_path: str = "investigations", days_threshold: int = 30):
        self.base_path = Path(base_path)
        self.days_threshold = days_threshold
        self.cutoff_date = datetime.now() - timedelta(days=days_threshold)
        
    def find_archivable_days(self) -> List[Path]:
        """Find investigation directories older than threshold."""
        archivable = []
        
        for year_dir in self.base_path.iterdir():
            if not year_dir.is_dir() or not year_dir.name.isdigit():
                continue
                
            for month_dir in year_dir.iterdir():
                if not month_dir.is_dir() or not month_dir.name.isdigit():
                    continue
                    
                for day_dir in month_dir.iterdir():
                    if not day_dir.is_dir() or not day_dir.name.isdigit():
                        continue
                    
                    # Parse date from directory structure
                    try:
                        dir_date = datetime(
                            int(year_dir.name),
                            int(month_dir.name), 
                            int(day_dir.name)
                        )
                        
                        if dir_date < self.cutoff_date:
                            # Check if not already archived
                            if not (day_dir / "investigations.tar.gz").exists():
                                archivable.append(day_dir)
                    except ValueError:
                        continue
                        
        return sorted(archivable)
    
    def parse_investigation_file(self, file_path: Path) -> Dict[str, Any]:
        """Extract key information from investigation markdown file."""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Extract metadata and key sections
            investigation_data = {
                'filename': file_path.name,
                'alert_id': self._extract_field(content, 'Alert ID'),
                'investigation_id': self._extract_field(content, 'Investigation ID'),
                'classification': self._extract_classification(content),
                'confidence': self._extract_field(content, 'Confidence'),
                'severity': self._extract_field(content, 'Assessed Severity'),
                'key_finding': self._extract_key_finding(content),
                'mitre_tactics': self._extract_mitre_tactics(content),
                'lessons_learned': self._extract_lessons_learned(content),
                'file_size': file_path.stat().st_size
            }
            
            return investigation_data
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return {'filename': file_path.name, 'error': str(e)}
    
    def _extract_field(self, content: str, field_name: str) -> str:
        """Extract field value from markdown content."""
        pattern = rf'\*\*{re.escape(field_name)}\*\*:\s*(.+?)(?:\n|$)'
        match = re.search(pattern, content)
        return match.group(1).strip() if match else "Unknown"
    
    def _extract_classification(self, content: str) -> str:
        """Extract classification with emoji indicators."""
        pattern = r'\*\*Classification\*\*:\s*([🟢🟡🔴]?\s*\*\*)?(\w+)'
        match = re.search(pattern, content)
        if match:
            return match.group(2).strip()
        return "Unknown"
    
    def _extract_key_finding(self, content: str) -> str:
        """Extract key finding summary."""
        pattern = r'\*\*Key Finding\*\*:\s*(.+?)(?:\n|$)'
        match = re.search(pattern, content)
        return match.group(1).strip() if match else "No summary available"
    
    def _extract_mitre_tactics(self, content: str) -> List[str]:
        """Extract MITRE ATT&CK tactics mentioned."""
        # Look for common MITRE tactics
        tactics = [
            'initial-access', 'execution', 'persistence', 'privilege-escalation',
            'defense-evasion', 'credential-access', 'discovery', 'lateral-movement',
            'collection', 'command-and-control', 'exfiltration', 'impact'
        ]
        
        found_tactics = []
        content_lower = content.lower()
        for tactic in tactics:
            if tactic in content_lower or tactic.replace('-', ' ') in content_lower:
                found_tactics.append(tactic)
        
        return found_tactics
    
    def _extract_lessons_learned(self, content: str) -> List[str]:
        """Extract lessons learned section."""
        lessons_section = re.search(r'## Lessons Learned\n(.+?)(?:\n##|\n---|\Z)', content, re.DOTALL)
        if lessons_section:
            lessons_text = lessons_section.group(1).strip()
            # Extract bullet points
            lessons = re.findall(r'^[-*]\s*(.+?)$', lessons_text, re.MULTILINE)
            return [lesson.strip() for lesson in lessons if lesson.strip()]
        return []
    
    def create_daily_summary(self, day_dir: Path, investigations: List[Dict[str, Any]]) -> str:
        """Create daily summary markdown file."""
        date_str = f"{day_dir.parent.parent.name}-{day_dir.parent.name:>02s}-{day_dir.name:>02s}"
        
        # Count classifications
        classifications = {'MALICIOUS': 0, 'SUSPICIOUS': 0, 'BENIGN': 0, 'UNKNOWN': 0}
        total_size = 0
        all_tactics = set()
        all_lessons = []
        
        investigations_summary = []
        
        for inv in investigations:
            if 'error' not in inv:
                class_key = inv['classification'].upper()
                if class_key in classifications:
                    classifications[class_key] += 1
                else:
                    classifications['UNKNOWN'] += 1
                
                total_size += inv.get('file_size', 0)
                all_tactics.update(inv.get('mitre_tactics', []))
                all_lessons.extend(inv.get('lessons_learned', []))
                
                investigations_summary.append({
                    'codename': inv['investigation_id'],
                    'alert_id': inv['alert_id'],
                    'classification': inv['classification'],
                    'confidence': inv['confidence'],
                    'key_finding': inv['key_finding'],
                    'filename': inv['filename']
                })
        
        # Create summary content
        summary_content = f"""# Daily Investigation Summary - {date_str}

**Archive Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}  
**Investigations Archived**: {len(investigations)}  
**Total Size Compressed**: {total_size / 1024:.1f} KB  

## Classification Summary

| Classification | Count |
|---------------|-------|
| 🔴 MALICIOUS | {classifications['MALICIOUS']} |
| 🟡 SUSPICIOUS | {classifications['SUSPICIOUS']} |
| 🟢 BENIGN | {classifications['BENIGN']} |
| ❓ UNKNOWN | {classifications['UNKNOWN']} |

## MITRE ATT&CK Tactics Observed

{', '.join(sorted(all_tactics)) if all_tactics else 'None identified'}

## Investigation Details

| Codename | Alert ID | Classification | Key Finding |
|----------|----------|---------------|-------------|
"""
        
        for inv in investigations_summary:
            summary_content += f"| {inv['codename']} | {inv['alert_id']} | {inv['classification']} | {inv['key_finding'][:80]}{'...' if len(inv['key_finding']) > 80 else ''} |\n"
        
        # Add lessons learned
        if all_lessons:
            summary_content += f"\n## Key Lessons Learned\n\n"
            for lesson in set(all_lessons[:10]):  # Top 10 unique lessons
                summary_content += f"- {lesson}\n"
        
        summary_content += f"""
## Accessing Archived Investigations

Original investigation files are compressed in `investigations.tar.gz`. To extract:

```bash
# Extract specific investigation
tar -xzf investigations.tar.gz <filename>.md

# Extract all investigations
tar -xzf investigations.tar.gz
```

---
*Summary generated by SOCdown archival tool*
"""
        
        return summary_content
    
    def archive_day(self, day_dir: Path, dry_run: bool = False) -> bool:
        """Archive investigations for a single day."""
        print(f"{'[DRY RUN] ' if dry_run else ''}Archiving {day_dir}")
        
        # Find all investigation markdown files
        investigation_files = [f for f in day_dir.glob("*.md") if not f.name.startswith("_")]
        
        if not investigation_files:
            print(f"  No investigation files found in {day_dir}")
            return False
        
        # Parse all investigations
        investigations = []
        for file_path in investigation_files:
            inv_data = self.parse_investigation_file(file_path)
            investigations.append(inv_data)
        
        # Create daily summary
        summary_content = self.create_daily_summary(day_dir, investigations)
        summary_file = day_dir / "_daily_summary.md"
        
        # Create compressed archive
        archive_file = day_dir / "investigations.tar.gz"
        
        if not dry_run:
            # Write summary
            summary_file.write_text(summary_content, encoding='utf-8')
            
            # Create tar.gz archive
            with tarfile.open(archive_file, 'w:gz') as tar:
                for file_path in investigation_files:
                    tar.add(file_path, arcname=file_path.name)
            
            # Remove original files
            for file_path in investigation_files:
                file_path.unlink()
        
        print(f"  {'Would create' if dry_run else 'Created'} summary: {summary_file.name}")
        print(f"  {'Would compress' if dry_run else 'Compressed'} {len(investigation_files)} investigations")
        
        return True
    
    def run_archival(self, dry_run: bool = False):
        """Run the archival process."""
        print(f"SOCdown Investigation Archiver")
        print(f"Archive threshold: {self.days_threshold} days")
        print(f"Cutoff date: {self.cutoff_date.strftime('%Y-%m-%d')}")
        print(f"Base path: {self.base_path.absolute()}")
        print()
        
        if not self.base_path.exists():
            print(f"Error: Investigation directory {self.base_path} not found")
            return False
        
        archivable_days = self.find_archivable_days()
        
        if not archivable_days:
            print("No investigations found that need archiving.")
            return True
        
        print(f"Found {len(archivable_days)} days to archive:")
        for day_dir in archivable_days:
            print(f"  {day_dir}")
        print()
        
        if dry_run:
            print("DRY RUN - No files will be modified")
            print()
        
        archived_count = 0
        for day_dir in archivable_days:
            if self.archive_day(day_dir, dry_run):
                archived_count += 1
        
        print(f"\n{'Would archive' if dry_run else 'Archived'} {archived_count} days of investigations")
        return True


def main():
    parser = argparse.ArgumentParser(description='Archive old SOC investigations')
    parser.add_argument('--days', type=int, default=30,
                       help='Archive investigations older than N days (default: 30)')
    parser.add_argument('--path', default='investigations',
                       help='Path to investigations directory (default: investigations)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be archived without making changes')
    
    args = parser.parse_args()
    
    archiver = InvestigationArchiver(args.path, args.days)
    success = archiver.run_archival(args.dry_run)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()