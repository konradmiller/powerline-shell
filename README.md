A Powerline style prompt for your shell
=======================================

A [Powerline](https://github.com/Lokaltog/vim-powerline) like prompt for Bash, ZSH and Fish, based on [powerline-shell](https://github.com/milkbikis/powerline-shell) by Shrey Banga:

![Powerline Screenshot](https://raw.githubusercontent.com/konradmiller/powerline-shell-proxy/master/bash-powerline-screenshot.png)


*  Shows some important details about the git/svn/hg/fossil branch:
    *  Displays the current branch which changes background color when the branch is dirty
    *  A '+' appears when untracked files are present
    *  When the local branch differs from the remote, the difference in number of commits is shown along with '⇡' or '⇣' indicating whether a git push or pull is pending
*  Changes color if the last command exited with a failure code
*  If you're too deep into a directory tree, shortens the displayed path with an ellipsis
*  Shows the current Python [virtualenv](http://www.virtualenv.org/) environment
*  It's easy to customize and extend. See below for details.

# Setup

This script uses ANSI color codes to display colors in a terminal. These are notoriously non-portable, so may not work for you out of the box, but try setting your $TERM to `xterm-256color`, because that works for me.

* Patch the font you use for your terminal: see https://github.com/Lokaltog/powerline-fonts
  * If you struggle too much to get working fonts in your terminal, you can use "compatible" mode.
  * If you're using old patched fonts, you have to use the older symbols. Basically reverse [this commit](https://github.com/milkbikis/powerline-shell/commit/2a84ecc) in your copy

* Clone this repository somewhere:

	git clone git@github.com:konradmiller/powerline-shell-proxy.git

* Copy `config.py.dist` to `config.py` and edit it to configure the segments you want. Then run

        ./install.py

  * This will generate `powerline-shell.py`

* (optional) Create a symlink to this python script in your home's bin:

        ln -s <path/to/powerline-shell.py> ~/bin/powerline-shell.py

  * If you don't want the symlink, just modify the path in the commands below

* For python2.6 you have to install argparse

        pip install argparse

* Finally, start the deamon

        ~/powerline-shell.py &


### All Shells:
There are a few optional arguments which can be seen by running `powerline-shell.py --help`.

```
  --cwd-only                        Only show the current directory
  --cwd-max-depth CWD_MAX_DEPTH     Maximum number of directories to show in path
  --colorize-hostname               Colorize the hostname based on a hash of itself
  --mode {patched,compatible,flat}  The characters used to make separators between segments
```

### Bash:
Add the following to your `.bashrc`:

```
export POWERLINE_SOCKET="$HOME/.powerline-daemon-socket-$(hostname)"

_powerline_prompt() {
	RET=$?  # save return code before calling whoami
	JOBS=$(($(ps -a -o ppid | grep $$ | wc -l)-1))
	PS1="$(echo $(whoami)";$$;$RET;bash;$PWD;$JOBS;$SSH_CLIENT" | nc -U $POWERLINE_SOCKET) "
}

export PROMPT_COMMAND="_powerline_prompt"
```

If you want to start the daemon from `.bashrc` add the following code above the
previous snippet:

```
export POWERLINE_PIDFILE="$HOME/.powerline-daemon-pid-$(hostname)"

start_powerline_daemon() {
	LANG=C setsid powerline-daemon.py &>/dev/null &
	echo $! > $POWERLINE_PIDFILE
	disown
}

command_exists () { hash "$1" &> /dev/null; }

if command_exists powerline-daemon.py; then
	if [[ ! -f "$POWERLINE_PIDFILE" ]]; then
		start_powerline_daemon
	else # pidfile exists
		ps -p $(cat "$POWERLINE_PIDFILE") &>/dev/null
		if [[ "$?" -ne 0 ]]; then
			# but daemon not running
			start_powerline_daemon
		fi
	fi
else
	echo "Install powerline :)"
fi
```

### Fish:
Redefine `fish_prompt` in `~/.config/fish/config.fish`:

```
function fish_prompt
	set s $status
	echo (whoami)";"(cut -d ' ' -f 4 /proc/self/stat)";$s;bare;$PWD;"(jobs -p | wc -l)";$SSH_CLIENT" | nc -U ~/.powerline-daemon-socket-(hostname)
end
```

# Customization

### Adding, Removing and Re-arranging segments

The `config.py` file defines which segments are drawn and in which order. Simply
comment out and rearrange segment names to get your desired arrangement. Every
time you change `config.py`, run `install.py`, which will generate a new
`powerline-shell.py` customized to your configuration. You should see the new
prompt immediately.

### Contributing new types of segments

The `segments` directory contains python scripts which are injected as is into
a single file `powerline-shell.py.template`. Each segment script defines a
function that inserts one or more segments into the prompt. If you want to add a
new segment, simply create a new file in the segments directory and add its name
to the `config.py` file at the appropriate location.

Make sure that your script does not introduce new globals which might conflict
with other scripts. Your script should fail silently and run quickly in any
scenario.

Make sure you introduce new default colors in `themes/default.py` for every new
segment you create. Test your segment with this theme first.

### Themes

The `themes` directory stores themes for your prompt, which are basically color
values used by segments. The `default.py` defines a default theme which can be
used standalone, and every other theme falls back to it if they miss colors for
any segments. Create new themes by copying any other existing theme and
changing the values. To use a theme, set the `THEME` variable in `config.py` to
the name of your theme.

A script for testing color combinations is provided at `themes/colortest.py`.
Note that the colors you see may vary depending on your terminal. When designing
a theme, please test your theme on multiple terminals, especially with default
settings.
