"""Responible for launching the server process."""

import subprocess, sys, os

shutdown_requested = False
while not shutdown_requested:
    server_process = subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "start_server.py")])
    out, errors = server_process.communicate()
    print(server_process.returncode, "return code", out, errors)
    shutdown_requested = server_process.returncode == 0
