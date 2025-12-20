#!/usr/bin/env python3
"""Documentation linter - verifies major .md files have required elements."""

import re
import sys
from pathlib import Path

MAJOR_PATHS = [
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "GOVERNANCE.md",
    "SUPPORT.md",
    "PRIVACY.md",
    "COMPLIANCE.md",
    "NOTICE.md",
    "THIRD_PARTY_NOTICES.md",
    "CITATION.md",
    "docs/**/*.md",
]

MINOR_PATHS = [
    ".github/*.md",
    "examples/**/*.md",
    "model_zoo/cards/*.md",
    "docs/figures/*.md",
]


def find_major_docs(root: Path) -> list[Path]:
    """Find all major documentation files."""
    major = []
    for pattern in MAJOR_PATHS:
        if "**" in pattern:
            major.extend(root.glob(pattern))
        else:
            p = root / pattern
            if p.exists():
                major.append(p)
    return major


def check_mermaid(content: str) -> bool:
    """Check for Mermaid diagram."""
    return "```mermaid" in content


def check_latex(content: str) -> bool:
    """Check for LaTeX formula."""
    return bool(re.search(r"\$[^$]+\$|\$\$[^$]+\$\$", content))


def check_table(content: str) -> bool:
    """Check for Markdown table."""
    return bool(re.search(r"\|.*\|.*\n\|[-:| ]+\|", content))


def lint_file(path: Path) -> list[str]:
    """Lint a single file and return issues."""
    issues = []
    content = path.read_text(encoding="utf-8")
    
    if not check_mermaid(content):
        issues.append(f"{path}: Missing Mermaid diagram")
    
    if not check_latex(content):
        issues.append(f"{path}: Missing LaTeX formula")
    
    if not check_table(content):
        issues.append(f"{path}: Missing Markdown table")
    
    return issues


def main() -> int:
    """Run docs lint."""
    root = Path(__file__).parent.parent
    major_docs = find_major_docs(root)
    
    print(f"Checking {len(major_docs)} major documentation files...")
    
    all_issues = []
    for doc in major_docs:
        issues = lint_file(doc)
        all_issues.extend(issues)
    
    if all_issues:
        print("\nIssues found:")
        for issue in all_issues:
            print(f"  - {issue}")
        return 1
    
    print("All docs pass lint checks!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
