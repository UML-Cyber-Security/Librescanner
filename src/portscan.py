# src/portscan.py
import socket

def check_port(host, port) -> int|None:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((host, port))
        s.close()
        return port
    except Exception:
        return None

def scan(host) -> list:
    open_ports = []
    for port in range(1, 65536):
        if check_port(host, port):
            open_ports.append(port)
    return open_ports
