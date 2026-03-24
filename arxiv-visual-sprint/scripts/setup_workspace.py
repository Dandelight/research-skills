#!/usr/bin/env python3
"""
工作目录初始化脚本
创建本次 sprint 的隔离目录及子结构。
"""

import sys
from datetime import datetime
from pathlib import Path

def setup_sprint_workspace(topic: str) -> str:
    # Sanitize topic
    safe_topic = "".join(c if c.isalnum() else "-" for c in topic).lower()
    safe_topic = safe_topic.strip("-")[:30]
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    dir_name = f"{date_str}-{safe_topic}"
    
    base_path = Path("./workspace/sprints")
    sprint_path = base_path / dir_name
    
    # Create directory structure
    sprint_path.mkdir(parents=True, exist_ok=True)
    (sprint_path / "raw").mkdir(exist_ok=True)
    (sprint_path / "extracted").mkdir(exist_ok=True)
    (sprint_path / "visuals").mkdir(exist_ok=True)
    
    print(f"✅ Created: {sprint_path}")
    return str(sprint_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python setup_workspace.py <topic>")
        sys.exit(1)
    
    print(setup_sprint_workspace(sys.argv[1]))
