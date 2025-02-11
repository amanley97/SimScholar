import os
import subprocess
import time
import shutil
from main.src.frontend import SimScholarFrontend
from main.utils.printdebug import printdebug

GEM5_DIR = os.path.join(os.getcwd(), "gem5")
GEM5_BIN = os.path.join(GEM5_DIR, "gem5_build", "gem5.opt")
M5OUT_DIR = os.path.join(os.getcwd(), "m5out")
GEMA_PORT = 8080

def remove_m5out():
    """Removes the 'm5out/' directory from the current working directory."""
    if os.path.exists(M5OUT_DIR) and os.path.isdir(M5OUT_DIR):
        try:
            shutil.rmtree(M5OUT_DIR)  # Remove the entire directory
            printdebug(f"[run] removed old m5 directory: {M5OUT_DIR}")
        except Exception as e:
            printdebug(f"[Error] failed to remove {M5OUT_DIR}: {e}", "red")
    else:
        printdebug(f"[Error] directory {M5OUT_DIR} does not exist, no need to clear.", "red")

def start_gem5():
    """Starts gem5 with the required command."""
    if not os.path.exists(GEM5_BIN):
        printdebug(f"[Error] gem5 binary not found at {GEM5_BIN}", "red")
        printdebug("[Error] Did you run 'setup'?", "red")
        exit(1)

    print(f"Starting gem5 with module 'gem5.utils.gema' on port {GEMA_PORT}...")
    
    gem5_process = subprocess.Popen(
        [GEM5_BIN, "-m", "gem5.utils.gema", str(GEMA_PORT), "--m5_override", os.getcwd()],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Give gem5 some time to initialize before starting the frontend
    time.sleep(5) 

    return gem5_process

if __name__ == "__main__":
    # Clean up m5 dir
    remove_m5out()

    # Start gema backend
    gem5_process = start_gem5()

    port = GEMA_PORT
    path = GEM5_DIR

    frontend = SimScholarFrontend(
        port=port, path=path
    )