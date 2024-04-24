# ----------------------------------------------------------------------------
# NOTICE: This code is the exclusive property of University of Kansas
#         Architecture Research and is strictly confidential.
#
#         Unauthorized distribution, reproduction, or use of this code, in
#         whole or in part, is strictly prohibited. This includes, but is
#         not limited to, any form of public or private distribution,
#         publication, or replication.
#
# For inquiries or access requests, please contact:
#         Alex Manley (amanley97@ku.edu)
#         Mahmudul Hasan (m.hasan@ku.edu)
# ----------------------------------------------------------------------------

import subprocess, time, os, shutil
from frontend.printdebug import printdebug
gem5 = os.getenv('GEM5_PATH')
snap_dir = os.getenv('SNAP')
snap_common = os.getenv('SNAP_USER_COMMON')
out_dir = str('--outdir='+snap_common+'/m5out')
frontend_path = os.path.join(snap_dir, 'frontend', 'frontend.py')
backend_path = os.path.join(snap_dir, 'api', 'backend.py')

path = {
    "backend" : backend_path,
    "frontend" : frontend_path
}

def run_backend():
    cmd = [str(gem5), out_dir, path["backend"]]
    printdebug("[Starting Backend]", color='green')
    p = subprocess.Popen(cmd)
    return p

def run_frontend():
    cmd = ["python3", path["frontend"]]
    printdebug("\n[Starting Frontend]", color='green')
    p = subprocess.Popen(cmd)
    p.wait()

def check_port(port):
    cmd = f"netstat -anp | grep :{port} | grep LISTEN"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = p.communicate()

    if p.returncode == 0 and output:  # Check if grep found anything
        printdebug(f"[Error] Port {port} is in use!", color='red')
        printdebug(f"[Error] Please kill the following process:\n{output}", color='red')
    else:
        printdebug(f"[run] Port {port} is available.\n", color='green')
    return p.returncode

def check_filetree():
    gsrc = os.path.join(os.getenv('SNAP'), 'exec', 'gem5.opt')
    gdst = os.path.join(os.getenv('SNAP_USER_COMMON'), 'gem5.opt')
    wsrc = os.path.join(os.getenv('SNAP'), 'workloads')
    wdst = os.path.join(os.getenv('SNAP_USER_COMMON'), 'workloads')

    if not os.path.exists(gdst):
        printdebug(f"[Error] gem5 binary missing, moving to correct location.", color='red')
        try:
            shutil.copy2(gsrc, gdst)
            printdebug(f'[run] Copied gem5 binary to {gdst}', color='green')
        except:
            printdebug(f'[Error] Failed to copy gem5 binary to {gdst}\n', color='red')
            return False
        if not os.path.exists(wdst):
            printdebug(f"[Error] Workloads directory missing, moving to correct location.", color='red')
            try:
                shutil.copytree(wsrc, wdst)
                printdebug(f'[run] Copied workloads to {wdst}', color='green')
            except:
                printdebug(f'[Error] Failed to copy workloads to {wdst}\n', color='red')
                return False
    printdebug(f'[run] gem5 binary and Workloads directory found!\n', color='green')
    return True

if __name__ == '__main__':
    port = 5000
    if check_port(port) and check_filetree():
        pb = run_backend()
        time.sleep(5)
        run_frontend()
        pb.kill()
