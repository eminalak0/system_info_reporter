# System Info Reporter

A beginner-friendly Python project that collects and reports your system information in a clean HTML table.

## Features

- Shows **operating system, CPU, RAM, and storage information**.
- Reports **usable RAM** and highlights **high RAM usage (>90%)**.
- Lists **all storage drives** with total, used, free, and usage percentage.
- Highlights **low disk space (<10 GB)** in red.
- Generates a **simple, readable HTML report**.

## Requirements

- Python 3.7+
- `psutil` library

Install psutil using:

```bash
python -m pip install psutil
