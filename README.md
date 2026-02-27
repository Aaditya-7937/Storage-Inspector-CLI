# Storage-Inspector

A Python-based command-line utility for recursive directory size analysis. This tool is designed to identify large storage consumers within nested system directories that are often bypassed by standard disk management tools.

## Description

Storage Inspector recursively traverses a specified path, calculates the total size of each top-level subdirectory, and provides color-coded feedback based on user-defined size thresholds. It includes robust error handling to skip system-restricted folders and junction points, preventing execution crashes due to PermissionErrors.

## Technical Features

* **Recursive Depth Calculation**: Accurately sums file sizes across deeply nested structures using `os.scandir`.
* **Exception Resilience**: Automatically handles `PermissionError` and `OSError` to ensure continuous execution in protected environments like `%LOCALAPPDATA%`.
* **Threshold-Based Reporting**: Categorizes directories into three states:
    * Optimal: < 500 MB
    * Warning: 500 MB - 2 GB
    * Critical: > 2 GB
* **Symbolic Link Awareness**: Skips symlinks and junction points to prevent infinite loops and redundant size reporting.

## Prerequisites

* Python 3.x
* colorama (for terminal-based color output)

## Installation

1. Clone the repository:
   git clone https://github.com/Aaditya-7937/Storage-Inspector-CLI.git

2. Install dependencies:
   pip install colorama

## Usage

Modify the target path in the script and execute:

python inspector.py

Example target for Windows users:
C:\Users\<Username>\AppData\Local

## License

MIT
