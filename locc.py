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
    """Aggregated stats for a group (extension or filename)"""
    name: str
    lines: int
    file_count: int

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

def is_binary(path: Path, chunk_size: int = 8192) -> bool:
    """Detect if a file is binary by checking for null bytes in the first chunk"""

    try:
        with path.open("rb") as f:
            chunk = f.read(chunk_size)
        return b"\x00" in chunk
    except (OSError, PermissionError):
        return True

def count_lines(path: Path) -> int | None:
    """Count lines in a file. Returns None if the file should be skipped"""

    try:
        if is_binary(path):
            return None
        
        text = path.read_text(encoding="utf-8")
        if not text:
            return 0

        count = text.count("\n")
        if not text.endswith("\n"):
            count += 1
        return count
    except UnicodeDecodeError:
        return None
    except (OSError, PermissionError):
        return None

def get_group_name(path: Path, group_by_file: bool) -> str:
    if group_by_file:
        return path.name
    if path.suffix:
        return path.suffix
    return "(no extension)"

def aggregate(results: list[CountResult], group_by_file: bool) -> list[GroupStats]:
    groups: dict[str, GroupStats] = {}
    for r in results:
        name = get_group_name(r.path, group_by_file)
        if name not in groups:
            groups[name] = GroupStats(name=name, lines=0, file_count=0)
        groups[name].lines += r.lines
        groups[name].file_count += 1
    return sorted(groups.values(), key=lambda g: g.lines, reverse=True)

### OUTPUT FORMATTING

def fmt(n: int) -> str:
    return f"{n:,}"

def _bar_color(pct: float) -> str:
    if pct >= 25:
        return "red"
    if pct >= 10:
        return "yellow"
    if pct >= 5:
        return "green"
    return "blue"

def render_results(groups: list[GroupStats], total_lines: int, total_files: int, skipped: int):
    """Render the results as a Rich table"""

    if not groups:
        console.print("[yellow]No countable files found[/]")
        return

    table = Table(title="[bold]Lines of Code[/]",show_header=True,header_style="bold cyan",border_style="bright white")
    table.add_column("Extension / File", style="bold white", no_wrap=True)
    table.add_column("Files", justify="right", style="cyan")
    table.add_column("%", justify="right", style="yellow")
    table.add_column("Distribution", ratio=1, min_width=20)

    max_lines = max(group.lines for group in groups)

    for group in groups:
        pct = (group.lines / total_files * 100) if total_files > 0 else 0.0
        bar_len = int((group.lines / max_lines ) * 30) if max_lines > 0 else 0
        bar = "#" * bar_len
        color = _bar_color(pct)

        table.add_row(group.name, fmt(group.file_count), fmt(group.lines), f"{pct:.1f}%", f"[{color}]{bar}[/]")

    table.add_section()
    table.add_row(
        "[bold white]Total[/]",
        f"[bold cyan]{fmt(total_files)}[/]",
        f"[bold green]{fmt(total_lines)}[/]",
        "",
    )

    console.print()
    console.print(table)

    if skipped > 0:
        console.print(f"\n[dim]{skipped} file(s) skipped (binary or unreadable)[/]")
