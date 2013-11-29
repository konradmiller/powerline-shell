import os

def add_username_segment():
    if powerline.args.shell == 'bash':
        user_prompt = ' \\u '
    elif powerline.args.shell == 'zsh':
        user_prompt = ' %n '
    else:
        user_prompt = ' %s ' % os.getenv('USER')

    if os.getenv('USER') != 'kmiller':
        powerline.append(user_prompt, Color.USERNAME_FG, Color.USERNAME_BG)

powerline.register( add_username_segment )
