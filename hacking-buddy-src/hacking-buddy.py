# hacking-buddy.py
# Generated leveraging GitHub Copilot and MCP documentation
# This script provides a simple interface to run some tools leveraging LLM capabilities.

import subprocess
from fastmcp import FastMCP

mcp = FastMCP("hacking-buddy-mcp")

# Port Scanning
## Masscan Scans
@mcp.tool()
def run_masscan_discovery(target):
    """Running masscan scan all port scan of ip range"""
    try:
        result = subprocess.run(
            ['sudo', 'masscan', '-sS', '-Pn', '--rate', "1000", "-p0-65535", target],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running masscan: {e.stderr}"

@mcp.tool()
def run_masscan_defined_ports(ports, target):
    """Running masscan defined port scan given port(s) of ip range"""
    try:
        result = subprocess.run(
            ['sudo', 'masscan', '-sS', '-Pn', '--rate', "1000", "-p", ports, target],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running masscan: {e.stderr}"

@mcp.tool()
def run_masscan_top_ports(top_ports, target):
    """Running masscan top-port scan given a top-ports integer of ip range"""
    try:
        result = subprocess.run(
            ['sudo', 'masscan', '-sS', '-Pn', '--rate', "1000", "--top-ports", top_ports, target],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running masscan: {e.stderr}"

## Nmap Scans
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

# dns_check: Bulk DNS existence check with bounded concurrency
@mcp.tool()
def dns_check(hostnames, record_types=None, timeout_ms=2000, concurrency=20, dns_servers=None, fast=True, require_any=True):
    """
    Bulk DNS existence check with bounded concurrency.
    Inputs:
      - hostnames: list of hostnames to check
      - record_types: list of DNS RR types to consider (default ["A","AAAA","CNAME"])
      - timeout_ms: per-query timeout in milliseconds (default 2000)
      - concurrency: max concurrent lookups (default 20)
      - dns_servers: optional list of DNS server IPs to use
      - fast: if True and require_any=True, stop after first hit per host
      - require_any: if True, any matching type => exists; if False, all requested types must match
    Returns:
      dict with "results" and "summary"
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import dns.resolver

    # Validate inputs
    if not isinstance(hostnames, (list, tuple)) or len(hostnames) == 0:
        return {"results": [], "summary": {"total": 0, "exists": 0, "missing": 0}}

    # Normalize options
    record_types = record_types or ["A", "AAAA", "CNAME"]
    try:
        record_types = [str(rt).upper().strip() for rt in record_types if str(rt).strip()]
    except Exception:
        record_types = ["A", "AAAA", "CNAME"]

    timeout = max(0.1, float(timeout_ms or 2000) / 1000.0)
    max_workers = max(1, int(concurrency or 20))

    def to_idna(h):
        try:
            return str(h).strip().encode("idna").decode("ascii")
        except Exception:
            return str(h).strip()

    def check_one(host):
        hostname = str(host).strip()
        ascii_host = to_idna(hostname)
        matched = []
        recs = []
        first_error = None
        try:
            res = dns.resolver.Resolver(configure=True)
            if dns_servers:
                try:
                    res.nameservers = list(dns_servers)
                except Exception:
                    pass
            for rtype in record_types:
                try:
                    answer = res.resolve(ascii_host, rtype, lifetime=timeout)
                    values = [r.to_text() for r in answer]
                    if values:
                        matched.append(rtype)
                        for v in values:
                            recs.append({"type": rtype, "value": v})
                        if fast and require_any:
                            break
                except Exception as e:
                    if first_error is None:
                        first_error = f"{type(e).__name__}: {e}"
            if require_any:
                exists = len(matched) > 0
            else:
                exists = all(rt in matched for rt in record_types)
            return {
                "hostname": hostname,
                "exists": bool(exists),
                "matchedTypes": matched,
                "records": recs,
                "error": None if exists or first_error is None else first_error,
            }
        except Exception as e:
            return {
                "hostname": hostname,
                "exists": False,
                "matchedTypes": [],
                "records": [],
                "error": f"{type(e).__name__}: {e}",
            }

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_map = {pool.submit(check_one, h): h for h in hostnames}
        for fut in as_completed(future_map):
            try:
                results.append(fut.result())
            except Exception as e:
                # Should not happen, but ensure we keep going
                results.append({
                    "hostname": str(future_map[fut]),
                    "exists": False,
                    "matchedTypes": [],
                    "records": [],
                    "error": f"{type(e).__name__}: {e}",
                })

    exists_count = sum(1 for r in results if r.get("exists"))
    summary = {"total": len(results), "exists": exists_count, "missing": len(results) - exists_count}
    return {"results": results, "summary": summary}

if __name__ == "__main__":
    mcp.run()
