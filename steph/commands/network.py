import socket
import subprocess
import psutil


class NetworkCommands:
    def get_commands(self) -> dict:
        return {
            "network_info": self.network_info,
            "network_speed": self.network_speed,
            "ping": self.ping,
            "connections": self.connections,
            "public_ip": self.public_ip,
        }

    def network_info(self, params: dict) -> str:
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        result = []
        for iface, addr_list in addrs.items():
            s = stats.get(iface)
            status = "UP" if s and s.isup else "DOWN"
            ips = [a.address for a in addr_list if a.family == socket.AF_INET]
            result.append(f"{iface} [{status}] IP: {', '.join(ips) if ips else 'N/A'}")
        return "\n".join(result) if result else "No network interfaces found."

    def network_speed(self, params: dict) -> str:
        counters = psutil.net_io_counters()
        return (
            f"Bytes Sent: {counters.bytes_sent / 1024**2:.1f} MB\n"
            f"Bytes Recv: {counters.bytes_recv / 1024**2:.1f} MB\n"
            f"Packets Sent: {counters.packets_sent}\n"
            f"Packets Recv: {counters.packets_recv}"
        )

    def ping(self, params: dict) -> str:
        host = params.get("host", "8.8.8.8")
        count = params.get("count", 4)
        try:
            result = subprocess.run(
                ["ping", "-n", str(count), host],
                capture_output=True, text=True, timeout=15
            )
            return result.stdout[-500:] if result.stdout else "Ping failed."
        except Exception as e:
            return f"Ping error: {e}"

    def connections(self, params: dict) -> str:
        cons = psutil.net_connections()
        result = []
        for c in cons[:20]:
            laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else "N/A"
            raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else "N/A"
            result.append(f"{c.type.name:8} {laddr:20} -> {raddr:20} {c.status or ''}")
        return "\n".join(result) if result else "No connections."

    def public_ip(self, params: dict) -> str:
        try:
            import requests
            r = requests.get("https://api.ipify.org", timeout=5)
            return f"Public IP: {r.text}"
        except:
            return "Could not determine public IP."
