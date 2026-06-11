import psutil
port = 8555
procs = []
for c in psutil.net_connections(kind='inet'):
    if c.laddr and c.laddr.port == port:
        try:
            p = psutil.Process(c.pid)
            procs.append((c.pid, p.name(), p.cmdline(), c.status))
        except Exception:
            procs.append((c.pid, '<unknown>', [], c.status))
print(procs)
