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

import subprocess, time, os
from frontend.printdebug import printdebug
gem5 = os.getenv('GEM5_PATH')
snap_dir = os.getenv('SNAP')
snap_common = os.getenv('SNAP_USER_COMMON')
out_dir = str('--outdir='+snap_common)
frontend_path = os.path.join(snap_dir, 'frontend', 'frontend.py')
backend_path = './api/backend.py'

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

if __name__ == '__main__':
    port = 5000
    if check_port(port):
        pb = run_backend()
        time.sleep(5)
        run_frontend()
        pb.kill()
