#!/usr/bin/env python3
"""
图像合规性验证脚本
"""

import sys
from pathlib import Path
from PIL import Image

def validate(filepath: str):
    path = Path(filepath)
    if not path.exists() or path.stat().st_size == 0:
        return False, "File empty or missing"
    
    try:
        with Image.open(filepath) as img:
            width, height = img.size
            ratio = width / height
            # 官方 3:2 允许微小偏差
            if abs(ratio - 1.5) > 0.05:
                return False, f"Invalid ratio: {ratio:.2f}"
            return True, f"Valid: {width}x{height}"
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    
    ok, msg = validate(sys.argv[1])
    print(f"{'✅' if ok else '❌'} {msg}")
    sys.exit(0 if ok else 1)
