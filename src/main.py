#!/usr/bin/env python3
"""
GitHub Topics Manager
Add topics to GitHub repositories easily and efficiently.
"""

import sys
from pathlib import Path

src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

# ruff: noqa: E402
from cli import run_cli


def main():
	run_cli()


if __name__ == "__main__":
	main()
