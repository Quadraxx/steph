import psutil
import os
import signal


class ProcessCommands:
    def get_commands(self) -> dict:
        return {
            "list_processes": self.list_processes,
            "kill_process": self.kill_process,
            "process_info": self.process_info,
            "top_processes": self.top_processes,
        }

    def list_processes(self, params: dict) -> str:
        sort_by = params.get("sort", "cpu")
        limit = params.get("limit", 20)
        procs = []
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                procs.append(p.info)
            except:
                pass
        if sort_by == "cpu":
            procs.sort(key=lambda x: x.get("cpu_percent", 0) or 0, reverse=True)
        elif sort_by == "memory":
            procs.sort(key=lambda x: x.get("memory_percent", 0) or 0, reverse=True)
        result = []
        for p in procs[:limit]:
            cpu = p.get("cpu_percent") or 0
            mem = p.get("memory_percent") or 0
            result.append(f"{p['pid']:6} {cpu:6.1f}% {mem:6.1f}% {p['name'][:30]}")
        return "\n".join(result)

    def top_processes(self, params: dict) -> str:
        params["sort"] = params.get("sort", "cpu")
        params["limit"] = params.get("limit", 10)
        return self.list_processes(params)

    def kill_process(self, params: dict) -> str:
        pid = params.get("pid")
        name = params.get("name")
        if pid:
            try:
                p = psutil.Process(int(pid))
                p.terminate()
                return f"Process {pid} terminated."
            except psutil.NoSuchProcess:
                return f"No process with PID {pid}."
            except Exception as e:
                return f"Error: {e}"
        elif name:
            killed = 0
            for p in psutil.process_iter(["pid", "name"]):
                try:
                    if p.info["name"] and name.lower() in p.info["name"].lower():
                        p.terminate()
                        killed += 1
                except:
                    pass
            return f"Killed {killed} process(es) matching '{name}'."
        return "Specify pid or name."

    def process_info(self, params: dict) -> str:
        pid = params.get("pid")
        if not pid:
            return "pid required."
        try:
            p = psutil.Process(int(pid))
            with p.oneshot():
                return (
                    f"PID: {p.pid}\n"
                    f"Name: {p.name()}\n"
                    f"Status: {p.status()}\n"
                    f"CPU: {p.cpu_percent()}%\n"
                    f"Memory: {p.memory_percent():.1f}%\n"
                    f"Threads: {p.num_threads()}\n"
                    f"Created: {p.create_time()}"
                )
        except psutil.NoSuchProcess:
            return f"No process with PID {pid}."
        except Exception as e:
            return f"Error: {e}"
