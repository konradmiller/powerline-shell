import os

def add_read_only_segment():
    cwd = powerline.cwd or os.getenv('PWD')

    if os.path.exists(cwd) and not os.access(cwd, os.W_OK):
        powerline.append(' %s ' % powerline.lock, Color.READONLY_FG, Color.READONLY_BG)

powerline.register( add_read_only_segment )
