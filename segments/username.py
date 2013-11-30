import os

def add_username_segment():
    if powerline.shell == 'bash':
        user_prompt = ' \\u '
    elif powerline.shell == 'zsh':
        user_prompt = ' %n '
    else:
        user_prompt = ' %s ' % powerline.user

    if os.getenv('USER') != 'kmiller':
        powerline.append(user_prompt, Color.USERNAME_FG, Color.USERNAME_BG)

powerline.register( add_username_segment )
