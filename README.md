# `locc` - Lines of Code Counter

A fast, beautiful command-line tool for counting lines of code in files and directories. 

## What It Does

`locc` scans your files and directories to provide a clear, visual breakdown of your codebase. Instead of a raw wall of text, it outputs a beautifully formatted, color-coded table showing exactly where your lines of code live.

### Key Features

*   **Simple Counting:** Counts all lines in a file (including blanks and comments), similar to `wc -l`.
*   **Smart Exclusions:** Automatically ignores dotfiles, dot directories (`.git`, `.venv`), and common dependency/build folders (`node_modules/`, `__pycache__/`, `build/`, `dist/`, etc.).
*   **Binary Detection:** Automatically skips binary files by checking for null-bytes and catching decode errors, ensuring your counts stay clean.
*   **Intelligent Grouping:** 
    *   When scanning directories, results are grouped by file extension (`.py`, `.js`, `.c`).
    *   When passing specific files, results are grouped by individual filenames.
    *   Files with no extension are grouped into `(no extension)`.
*   **Rich Visual Output:** Displays a formatted table using the Rich library, showing file counts, total lines, percentages, and distribution bars. Results are sorted by highest line count.
*   **Progress Indicators:** Displays transient progress bars while scanning and counting large directories so you always know what's happening.
*   **Resilient:** Gracefully skips files and directories with permission errors without crashing the whole scan.

### Customization Options

*   **Custom Exclusions:** Add your own glob patterns to exclude specific files or directories (e.g., ignore `*.test.js` or `tests/`).
*   **Depth Limiting:** Restrict how deep the tool recurses into subdirectories (e.g., only scan the top-level folder, or limit to 3 levels deep).

---

*(Installation and usage examples to be added)*
