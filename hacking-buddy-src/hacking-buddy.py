# hacking-buddy.py
# Generated leveraging GitHub Copilot and MCP documentation
# This script provides a simple interface to run some tools leveraging LLM capabilities.

import subprocess
from fastmcp import FastMCP

mcp = FastMCP("hacking-buddy-mcp")

# Nmap Scans
@mcp.tool()
def run_nmap(target):
    """Running nmap service scan on a target."""
    try:
        result = subprocess.run(
            ['nmap', '-sV', target],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running Nmap: {e.stderr}"
    
@mcp.tool()
def run_nmap_discovery(target):
    """Running nmap discovery scan of ip range"""
    try:
        result = subprocess.run(
            ['nmap', '-sn', '-oG', '-', target],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running Nmap: {e.stderr}"
    
@mcp.tool()
def run_banner_grabbing(target):
    """Running nmap banner grab on a target."""
    try:
        result = subprocess.run(
            ['nmap', '-sV', '--script=banner', target],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running banner grabbing: {e.stderr}"

    
@mcp.tool()
def run_smb_scan(target, ports='445'):
    """Running nmap smb scan on a target."""
    try:
        result = subprocess.run(
            ['nmap', '-p', ports, '--script', 'smb-enum-shares,smb-enum-users,smb-os-discovery', target],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running SMB scan: {e.stderr}"
    
################################################################################################################

# sqlmap
@mcp.tool()
def run_sqlmap(target, dbms=None):
    """Running sqlmap on a target."""
    command = ['sqlmap', '-u', target, '-v', '5'] #If getting errors like 401, we can ignore by using `--nocode 401`
    if dbms:
        command.extend(['--dbms', dbms])
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running sqlmap: {e.stderr}"

################################################################################################################

# Kubernetes (K8s)
@mcp.tool()
def run_kubectl_enumeration():
    """Run basic kubectl enumeration commands."""
    commands = [
        ("Pods", ["kubectl", "get", "pods"]),
        ("Deployments", ["kubectl", "get", "deployments"]),
        ("ReplicaSets", ["kubectl", "get", "replicasets"]),
        ("Auth Can-I", ["kubectl", "auth", "can-i", "--list"]),
    ]
    output = []
    for name, cmd in commands:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            output.append(f"== {name} ==\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            output.append(f"== {name} ==\nError: {e.stderr}")
    return "\n".join(output)

################################################################################################################

# DNS
@mcp.tool()
def check_dns_info(target):
    """Check DNS information for a target and determine if it is publicly available."""
    import socket
    import dns.resolver
    result = []
    try:
        # Try to resolve A record
        a_records = dns.resolver.resolve(target, 'A')
        ips = [r.to_text() for r in a_records]
        result.append(f"A records: {ips}")
        public = True if ips else False
    except Exception as e:
        result.append(f"A record lookup failed: {e}")
        public = False
    # Try to resolve AAAA record
    try:
        aaaa_records = dns.resolver.resolve(target, 'AAAA')
        ipv6s = [r.to_text() for r in aaaa_records]
        result.append(f"AAAA records: {ipv6s}")
    except Exception as e:
        result.append(f"AAAA record lookup failed: {e}")
    # Try to resolve MX record
    try:
        mx_records = dns.resolver.resolve(target, 'MX')
        mxs = [r.to_text() for r in mx_records]
        result.append(f"MX records: {mxs}")
    except Exception as e:
        result.append(f"MX record lookup failed: {e}")
    # Try to resolve TXT record
    try:
        txt_records = dns.resolver.resolve(target, 'TXT')
        txts = [r.to_text() for r in txt_records]
        result.append(f"TXT records: {txts}")
    except Exception as e:
        result.append(f"TXT record lookup failed: {e}")
    # Public availability
    if public:
        result.append(f"Status: Host {target} is publicly available (A record found).")
    else:
        result.append(f"Status: Host {target} is NOT publicly available (no A record found).")
    return "\n".join(result)

if __name__ == "__main__":
    mcp.run()