import os

def get_short_path(cwd):
    home = os.getenv('HOME')
    names = cwd.split(os.sep)
    if names[0] == '': names = names[1:]
    path = ''
    for i in range(len(names)):
        path += os.sep + names[i]
        try:
            if os.path.samefile(path, home):
                return ['~'] + names[i+1:]
        except:
            pass
    if not names[0]:
        return ['/']
    return names

def add_cwd_segment():
    letters = False # set to True to emulate "fish" like cwd
    cwd = powerline.cwd or os.getenv('PWD')
    names = get_short_path(cwd.decode('utf-8'))

    max_depth = powerline.args.cwd_max_depth
    long_names = names
    if len(names) > max_depth:
        if letters is True:
            names = names[:1] + [name[0:1] for name in names[1:1 - max_depth]] + names[1 - max_depth:]
        else:
            names = names[:1] + [u'\u2026'] + names[1 - max_depth:]

    path = ''
    if not powerline.args.cwd_only:
        for i in range(len(names)-1):
            n = names[i]

            # for each component, check if we still have a valid path
            if long_names[i] == '~':
                path = os.getenv('HOME') # ~ is always the first element, so no need to append
            else:
                path += os.sep + long_names[i]

            # Background color of path segment
            if os.path.exists(path):
                col = Color.PATH_BG
            else:
                col = Color.CMD_FAILED_BG
                
            # We need a different separator if the background color changes between this segment and the next
            if os.path.exists(path) == os.path.exists(path + os.sep + long_names[i + 1]):
                sep = powerline.separator_thin
                sep_col = Color.SEPARATOR_FG
            else:
                sep = powerline.separator
                sep_col = Color.PATH_BG
            
            if n == '~' and Color.HOME_SPECIAL_DISPLAY:
                powerline.append(' %s ' % n, Color.HOME_FG, Color.HOME_BG)
            else:
                powerline.append(' %s ' % n, Color.PATH_FG, col,
                    sep, sep_col)

    path += os.sep + long_names[-1]

    if names[-1] == '~' and Color.HOME_SPECIAL_DISPLAY:
        powerline.append(' %s ' % names[-1], Color.HOME_FG, Color.HOME_BG)
    else:
        if os.path.exists(path):
            powerline.append(' %s' % names[-1], Color.CWD_FG, Color.PATH_BG)
        else:
            powerline.append(' %s' % names[-1], Color.CWD_FG, Color.CMD_FAILED_BG)

powerline.register( add_cwd_segment )
