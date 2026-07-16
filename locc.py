#!/usr/bin/env python
"""locc - Lines of Code Counter"""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass
from pathlib import Path
from collections.abc import Iterator, Sequence

import typer
from rich.console import Console
from rich.progress import (BarColumn, SpinnerColumn, TextColumn, TimeElapsedColumn)
from rich.table import Table

app = typer.Typer(name="locc", help="Count lines of code in files and directories", add_completion=False, no_args_is_help=False)
console = Console()

DEFAULT_EXCLUDED_DIRS = {
    "node_modules",
    "__pycache__",
    "target",
    "build",
    ".pytest_cache",
    ".mypy_cache",
}

@dataclass
class CountResult:
    """Result of counting a single file"""
    path: Path
    line: int

@dataclass
class GroupStats:
    """Aggregated stats for a group (extention or filename)"""
    name: str
    lines: int
    file_count: int

# FILE STUFF

def is_excluded(name: str, patterns: Sequence[str]) -> bool:
    """check if a file/dir name should be excluded based on defaults and patterns"""

    if name.startswith("."):
        return True
    if name in DEFAULT_EXCLUDED_DIRS:
        return True
    
    for pattern in patterns:
        if pattern.endswith("/"):
            if name == pattern.rstrip("/"):
                return True
        elif fnmatch.fnmatch(name, pattern):
            return True
    return False

def walk_directory(root: Path, patterns: Sequence[str], max_depth: int | None) -> Iterator[Path]:
    """Walk a directory yielding file paths, respecting exclusions and depth"""

    def _walk(current: Path, depth: int) -> Iterator[Path]:
        if max_depth is not None and depth > max_depth:
            return
        
        try:
            entries = sorted(current.iterdir())
        except (PermissionError, OSError):
            return

        for entry in entries:
            if is_excluded(entry.name, patterns):
                continue
            if entry.is_symlink():
                continue
            
            try:
                if entry.is_dir():
                    yield from _walk(entry, depth + 1)
                elif entry.is_file(): 
                    yield entry
            except (PermissionError, OSError):
                continue
    yield from _walk(root, 0)

def discover_files(paths: Sequence[Path], patterns: Sequence[str], max_depth: int | None) -> list[Path]:
    """Discover all files to count from the given paths"""

    files: list[Path] = []

    for path in paths:
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(walk_directory(path, patterns, max_depth))
        else:
            console.print(f"[yellow]Warning:[/yellow] '{path}' is not a file or directory, skipping")
    return files
