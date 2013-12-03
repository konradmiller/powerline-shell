import os
import re
import subprocess

def add_jobs_segment():
#    pppid = str(powerline.bashpid)
#    output = subprocess.Popen(['ps', '-a', '-o', 'ppid'], stdout=subprocess.PIPE).communicate()[0]
#    num_jobs = len(re.findall(str(pppid), output)) - 1
    num_jobs = powerline.jobs
    if num_jobs > 0:
        powerline.append(' %d ' % num_jobs, Color.JOBS_FG, Color.JOBS_BG)

powerline.register(add_jobs_segment)
