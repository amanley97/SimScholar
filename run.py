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
