# LOC Counter (locc)

A fast, beautiful lines of code counter with rich terminal output and smart filtering.

## Features

- **Rich terminal output** with color-coded distribution bars
- **Smart file detection** - automatically skips binary files
- **Default exclusions** for common directories (`node_modules`, `__pycache__`, etc.)
- **Flexible filtering** with glob patterns
- **Depth limiting** for directory traversal
- **Aggregated statistics** by file extension (or filename)
- **Progress indicators** for long-running scans
- **Gruvbox-inspired color scheme** for readability

## Installation

### From Source

```bash
# Clone the repository
git clone <repository-url>
cd locc

# Install in development mode
pip install -e .
```

### Direct Usage

If you prefer not to install, you can run directly:

```bash
python locc.py [options]
```

### Dependencies

- **rich** >= 13.0.0 - Terminal formatting
- **typer** >= 0.9.0 - CLI framework

These will be installed automatically when you run `pip install -e .`.

## Usage

### Basic Examples

```bash
# Scan current directory
locc

# Scan specific directory
locc ~/projects

# Scan specific files
locc foo.py bar.py

# Exclude test files
locc -e '*.test.js'

# Multiple exclusion patterns
locc -e '*.lock' -e 'vendor/'

# Limit depth to 2 levels
locc -d 2

# Combine options
locc ~/src -e '*.pyc' -e '__pycache__/' -d 3
```

### Options

| Option          | Description                                               |
|-----------------|-----------------------------------------------------------|
| `paths`         | Files or directories to scan (default: current directory) |
| `-e, --exclude` | Glob patterns to exclude (repeatable)                     |
| `-d, --depth`   | Maximum recursion depth                                   |

### Default Exclusions

The tool automatically excludes these directories:
- `node_modules`
- `__pycache__`
- `target`
- `build`
- `.pytest_cache`
- `.mypy_cache`
- All hidden directories/files (starting with `.`)

## Output Example

```
════════════════════════════════════════════════════════════════
                    Lines of Code                     
════════════════════════════════════════════════════════════════
Extension / File  Files  Lines     %  Distribution             
────────────────────────────────────────────────────────────────
.py                  12    2,450  45.2%  ######################
.js                   8    1,200  22.1%  ###########           
.go                   5      890  16.4%  #########             
.rs                   3      450   8.3%  ####                   
(no extension)        2      180   3.3%  ##                     
.md                   4      144   2.7%  #                      
.yml                  3       60   1.1%                          
────────────────────────────────────────────────────────────────
Total                37    5,374                                

5 file(s) skipped (binary or unreadable)
```

## Technical Details

- **Binary detection**: Checks for null bytes in first 8KB of file
- **Encoding**: UTF-8 only (skips files with encoding errors)
- **Line counting**: Counts newline characters, adds 1 if file doesn't end with newline
- **Symlinks**: Skipped for safety
- **Performance**: Uses streaming reads with configurable chunk sizes

---

## Why locc?

- **Fast**: Optimized for large codebases
- **Beautiful**: Color-coded output makes results easy to read
- **Practical**: Smart defaults with flexible customization
- **Single file**: Easy to copy and use anywhere
