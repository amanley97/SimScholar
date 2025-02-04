import os
import subprocess
import time
from main.src.frontend import SimScholarFrontend
from main.utils.printdebug import printdebug

GEM5_DIR = os.path.join(os.getcwd(), "gem5")
GEM5_BIN = os.path.join(GEM5_DIR, "gem5_build", "gem5.opt")
GEMA_PORT = 8080

def start_gem5():
    """Starts gem5 with the required command."""
    if not os.path.exists(GEM5_BIN):
        printdebug(f"[Error] gem5 binary not found at {GEM5_BIN}", "red")
        printdebug("[Error] Did you run 'setup'?", "red")
        exit(1)

    print(f"Starting gem5 with module 'gem5.utils.gema' on port {GEMA_PORT}...")
    
    gem5_process = subprocess.Popen(
        [GEM5_BIN, "-m", "gem5.utils.gema", str(GEMA_PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Give gem5 some time to initialize before starting the frontend
    time.sleep(2) 

    return gem5_process

if __name__ == "__main__":
    gem5_process = start_gem5()

    port = GEMA_PORT
    path = GEM5_DIR

    frontend = SimScholarFrontend(
        port=port, path=path
    )

    # Wait for gem5 to finish execution
    gem5_process.wait()