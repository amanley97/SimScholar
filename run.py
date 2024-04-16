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
def prRed(skk): print("\033[91m{}\033[00m".format(skk))
def prGreen(skk): print("\033[92m{}\033[00m".format(skk))

path = {
    "backend" : "./api/backend.py",
    "frontend" : "./frontend/frontend.py"
}

def run_backend():
    cmd = ["gem5.opt", path["backend"]]
    prGreen("[Starting Backend]")
    p = subprocess.Popen(cmd)
    return p

def run_frontend():
    cmd = ["python3", path["frontend"]]
    prGreen("\n[Starting Frontend]")
    p = subprocess.Popen(cmd)
    p.wait()

def check_port(port):
    cmd = f"sudo netstat -anp | grep :{port} | grep LISTEN"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = p.communicate()

    if p.returncode == 0 and output:  # Check if grep found anything
        prRed("[Error]")
        print(f"Port {port} is in use!\n")
        print(f"Please kill the following process:\n{output}")
    else:
        print(f"Port {port} is available.\n")
    return p.returncode

if __name__ == '__main__':
    port = 5000
    if check_port(port):
        pb = run_backend()
        time.sleep(5)
        run_frontend()
        pb.kill()
