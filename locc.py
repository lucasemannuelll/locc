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
