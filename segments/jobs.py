import os
import re
import subprocess

def add_jobs_segment():
    num_jobs = powerline.jobs
    if num_jobs > 0:
        powerline.append(' %d ' % num_jobs, Color.JOBS_FG, Color.JOBS_BG)

powerline.register(add_jobs_segment)
