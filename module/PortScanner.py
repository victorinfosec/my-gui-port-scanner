import socket
import concurrent.futures
import threading
import customtkinter as ctk
import nmap


class PortScanner:
    """Classe responsable des scans de ports et services."""

    def __init__(self):
        self.scanning = False  # État du scan

    def scan_port(self, domainip: str, port: int) -> tuple:
        """Scanne un port unique."""
        try:
            s = socket.create_connection((domainip, port), timeout=0.5)
            return (port, "open")
        except Exception:
            return (port, "closed")

    def scan_ports(self, ip, start_port, end_port):
        """Scanne une plage de ports."""
        open_ports = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.scan_port, ip, port): port for port in range(start_port, end_port + 1)}
            for future in concurrent.futures.as_completed(futures):
                if not self.scanning:
                    break
                port, status = future.result()
                if status == "open":
                    open_ports[port] = status
        return open_ports

    def scan_services(self, ip, open_ports):
        """Scanne les services associés aux ports ouverts."""
        nm = nmap.PortScanner()
        services = {}
        for port in open_ports:
            nm.scan(ip, str(port))
            if nm[ip].all_state() == 'up':
                service_info = nm[ip]['tcp'][port]
                services[port] = {
                    'name': service_info['name'],
                    'state': service_info['state'],
                    'version': service_info.get('version', 'N/A')
                }
        return services
