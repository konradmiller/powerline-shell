import os

def add_username_segment():
    if powerline.shell == 'bash':
        user_prompt = ' \\u '
    elif powerline.shell == 'zsh':
        user_prompt = ' %n '
    else:
        user_prompt = ' %s ' % powerline.user

    if powerline.user == 'root':
        bgcolor = Color.USERNAME_ROOT_BG
    else:
        bgcolor = Color.USERNAME_BG

    if os.getenv('USER') != 'kmiller':
        powerline.append(user_prompt, Color.USERNAME_FG, bgcolor)

powerline.register( add_username_segment )
