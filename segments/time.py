# From pull request to https://github.com/milkbikis/powerline-shell
# by https://github.com/filipebarros

def add_time_segment():
    if powerline.shell == 'bash':
        time = ' \\t '
    elif powerline.shell == 'zsh':
        time = ' %* '
    else:
        import time
        time = ' %s ' % time.strftime('%H:%M:%S')

    powerline.append(time, Color.HOSTNAME_FG, Color.HOSTNAME_BG)

powerline.register( add_time_segment )
