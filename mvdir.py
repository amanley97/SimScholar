import os
import shutil

def move_gem5():
    src = os.path.join(os.getenv('SNAP'), 'exec', 'gem5.opt')
    dst = os.path.join(os.getenv('SNAP_USER_COMMON'), 'gem5.opt')

    if not os.path.exists(dst):
        shutil.copy2(src, dst)
        print(f'copied gem5 binary to {dst}')
    else:
        print(f'gem5 binary already present at {dst}')

def move_workloads():
    src = os.path.join(os.getenv('SNAP'), 'workloads')
    dst = os.path.join(os.getenv('SNAP_USER_COMMON'), 'workloads')

    if not os.path.exists(dst):
        shutil.copytree(src, dst)
        print(f'copied workloads to {dst}')
    else:
        print(f'Workloads already present at {dst}')

if __name__ == '__main__':
    move_workloads()
    move_gem5()
