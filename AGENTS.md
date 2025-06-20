# AGENTS.MD

## Project Overview

**Hacking Buddy MCP** is a proof-of-concept AI-powered toolkit for Red Team and Pentesting workflows. It integrates with the FastMCP framework to provide automated security tools for reconnaissance, exploitation, and analysis.

## How the Project Works

- The main entry point is [`hacking-buddy-src/hacking-buddy.py`](hacking-buddy-src/hacking-buddy.py).
- Tools are defined as Python functions decorated with `@mcp.tool()`.
- Each tool typically takes a `target` argument and returns output as a string.
- Tools leverage external command-line utilities (e.g., `nmap`, `sqlmap`, `kubectl`) or Python libraries (e.g., `dnspython`).
- The MCP agent is started by running the script directly.

## Adding or Modifying Tools

- Define a new function with the `@mcp.tool()` decorator.
- Implement the tool logic (call subprocesses or use Python libraries).
- Add a docstring describing the tool’s purpose and usage.
- Register the tool by ensuring it is imported and decorated.
- For DNS-related tools, use the `dnspython` library for record lookups.

## Example Tool: DNS Information

- The `check_dns_info(target)` tool queries A, AAAA, MX, and TXT DNS records for a target.
- It determines if the host is publicly available by checking for A records.
- Output is a summary of DNS records and public status.

## Setup

- Use `uv` for dependency management and virtual environments.
- Install dependencies with `uv pip install -r pyproject.toml`.
- Ensure `fastmcp` and any required libraries (e.g., `dnspython`) are installed.

## Next Steps

- When given a task, analyze the tool structure in `hacking-buddy.py`.
- Add or modify tools as needed, following the established pattern.
- Ensure new tools are registered and tested via the MCP interface.