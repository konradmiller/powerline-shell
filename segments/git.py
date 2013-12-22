import re
import subprocess
import os

def get_valid_cwd(cwd):
    """ We check if the current working directory is valid or not. Typically
        happens when you checkout a different branch on git that doesn't have
        this directory.
        We return the longest valid prefix of the current cwd.
    """
    parts = cwd.split(os.sep)
    while parts and not os.path.exists(cwd):
        parts.pop()
        cwd = os.sep.join(parts)
    return cwd

def get_git_status():
    has_pending_commits = True
    has_untracked_files = False
    origin_position = ""
    git_env = os.environ
    git_env["LANG"] = "en_US"
    output = subprocess.Popen(['git', 'status', '--ignore-submodules'],
            stdout=subprocess.PIPE, env=git_env).communicate()[0]
    for line in output.split('\n'):
        origin_status = re.findall(
                r"Your branch is (ahead|behind).*?(\d+) comm", line)
        if origin_status:
            origin_position = " %d" % int(origin_status[0][1])
            if origin_status[0][0] == 'behind':
                origin_position += u'\u21E3'
            if origin_status[0][0] == 'ahead':
                origin_position += u'\u21E1'

        if line.find('nothing to commit') >= 0:
            has_pending_commits = False
        if line.find('Untracked files') >= 0:
            has_untracked_files = True
    return has_pending_commits, has_untracked_files, origin_position


def add_git_segment():
    # fast path
    oldcwd = os.getcwd()
    os.chdir(get_valid_cwd(powerline.cwd))
    found = False
    while os.getcwd() != '/':
        if os.access( ".git", os.R_OK ):
            found = True
            break
        os.chdir('..')

    if not found:
        return

    try:
        #cmd = "git branch 2> /dev/null | grep -e '\\*'"
#        os.chdir(powerline.cwd)
        p1 = subprocess.Popen(['git', 'branch', '--no-color'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p2 = subprocess.Popen(['grep', '-e', '\\*'], stdin=p1.stdout, stdout=subprocess.PIPE)
        output = p2.communicate()[0].strip()
        if not output:
            return

        branch = output.rstrip()[2:]
        has_pending_commits, has_untracked_files, origin_position = get_git_status()
        branch += origin_position
        if has_untracked_files:
            branch += ' +'

        bg = Color.REPO_CLEAN_BG
        fg = Color.REPO_CLEAN_FG
        if has_pending_commits:
            bg = Color.REPO_DIRTY_BG
            fg = Color.REPO_DIRTY_FG

        str = u'\uE0A0 ' + branch
        os.chdir(oldcwd)
        powerline.append(' %s ' % str, fg, bg)
    except OSError:
        os.chdir(oldcwd)
    except subprocess.CalledProcessError:
        os.chdir(oldcwd)

powerline.register( add_git_segment )
