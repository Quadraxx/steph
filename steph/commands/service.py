import subprocess
import psutil


class ServiceCommands:
    def get_commands(self) -> dict:
        return {
            "list_services": self.list_services,
            "service_status": self.service_status,
            "start_service": self.start_service,
            "stop_service": self.stop_service,
            "restart_service": self.restart_service,
            "disk_usage": self.disk_usage,
            "disk_info": self.disk_info,
            "battery": self.battery,
            "system_uptime": self.system_uptime,
        }

    def _run_sc(self, action: str, service: str) -> str:
        try:
            result = subprocess.run(
                ["sc", action, service],
                capture_output=True, text=True, timeout=10
            )
            output = (result.stdout or result.stderr).strip()
            return output[:500] if output else f"{action} {service}"
        except Exception as e:
            return f"Error: {e}"

    def list_services(self, params: dict) -> str:
        try:
            result = subprocess.run(
                ["sc", "query", "type=", "service", "state=", "all"],
                capture_output=True, text=True, timeout=15
            )
            lines = result.stdout.splitlines()
            services = []
            for line in lines:
                if "SERVICE_NAME" in line:
                    name = line.split(":")[1].strip()
                    services.append(name)
            out = "\n".join(services)
            return out[:1500] if out else "No services found."
        except Exception as e:
            return f"Error: {e}"

    def service_status(self, params: dict) -> str:
        name = params.get("name") or params.get("service")
        if not name:
            return "service name required."
        return self._run_sc("query", name)

    def start_service(self, params: dict) -> str:
        name = params.get("name") or params.get("service")
        if not name:
            return "service name required."
        return self._run_sc("start", name)

    def stop_service(self, params: dict) -> str:
        name = params.get("name") or params.get("service")
        if not name:
            return "service name required."
        return self._run_sc("stop", name)

    def restart_service(self, params: dict) -> str:
        name = params.get("name") or params.get("service")
        if not name:
            return "service name required."
        stop = self._run_sc("stop", name)
        start = self._run_sc("start", name)
        return f"{stop}\n{start}"

    def disk_usage(self, params: dict) -> str:
        path = params.get("path", "/")
        parts = psutil.disk_partitions()
        result = []
        for p in parts:
            try:
                usage = psutil.disk_usage(p.mountpoint)
                result.append(
                    f"{p.device:10} {p.mountpoint:20} "
                    f"{usage.used // 1024**3:>4}GB / {usage.total // 1024**3:>4}GB "
                    f"({usage.percent:.0f}%)"
                )
            except:
                pass
        return "\n".join(result) if result else "No disk info."

    def disk_info(self, params: dict) -> str:
        return self.disk_usage(params)

    def battery(self, params: dict) -> str:
        if not psutil.sensors_battery():
            return "No battery detected."
        batt = psutil.sensors_battery()
        plugged = "Plugged In" if batt.power_plugged else "On Battery"
        return f"Battery: {batt.percent:.0f}% ({plugged})"

    def system_uptime(self, params: dict) -> str:
        uptime_seconds = int(psutil.boot_time())
        from datetime import datetime
        boot = datetime.fromtimestamp(uptime_seconds)
        delta = datetime.now() - boot
        days = delta.days
        hours = delta.seconds // 3600
        minutes = (delta.seconds // 60) % 60
        return f"Uptime: {days}d {hours}h {minutes}m (boot: {boot.strftime('%Y-%m-%d %H:%M')})"
