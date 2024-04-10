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

import subprocess, time
path = {
    "backend" : "./api/obtain-api.py",
    "frontend" : "./frontend/frontend.py"
}

def run_backend():
    cmd = ["gem5.opt", path["backend"]]
    print("Starting backend")
    p = subprocess.Popen(cmd)
    return p

def run_frontend():
    cmd = ["python3", path["frontend"]]
    print("Starting Frontend")
    p = subprocess.Popen(cmd)
    p.wait()

if __name__ == '__main__':
    pb = run_backend()
    time.sleep(5)
    run_frontend()
    pb.kill()
