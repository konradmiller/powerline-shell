import os

def add_ssh_segment():

    if os.getenv('SSH_CLIENT'):
        str = powerline.network + " \\h ";
        powerline.append(' %s ' % str, Color.SSH_FG, Color.SSH_BG)

powerline.register( add_ssh_segment )
