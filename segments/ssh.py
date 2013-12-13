import os

def add_ssh_segment():

    if powerline.ssh:
        import socket

        if powerline.shell == 'bash':
            host_prompt = ' \\h '
        elif powerline.shell == 'zsh':
            host_prompt = ' %m '
        else:
            import socket
            host_prompt = ' %s ' % powerline.hostname

        str = powerline.network + host_prompt

        powerline.append(' %s ' % str, Color.SSH_FG, Color.SSH_BG)

powerline.register( add_ssh_segment )
