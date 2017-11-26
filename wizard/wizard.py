import cmd
import glob
import logging
import subprocess
import six
import sys
#import libtmux
import os

from wizard.settings import *
from wizard.i3 import utils as i3utils


logging.basicConfig(format='-[%(prompt)s] %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _run_in_tmux(name, command, return_output=False):
    if isinstance(command, six.string_types):
        command = command.split(" ")
    out = subprocess.Popen(["tmux", "new", "-s", name, "-d"] + command)
    if return_output:
        return out

def _i3_restart():
    subprocess.Popen(['i3-msg', 'restart'])

def _replace_i3_config(replace_version):
    config = os.path.join(I3DIR, 'config')
    config_backup = os.path.join(I3DIR, 'config_backup')
    config_new = os.path.join(I3DIR, "config_{}".format(replace_version))
    subprocess.Popen(['cp', config, config_backup])
    assert os.path.exists(config_new), replace_version + " does not exist"
    subprocess.Popen(['cp', config_new, config])
    _i3_restart()

def _gen_i3_config(replace_version):
    i3utils.copy_config(replace_version)
    _i3_restart()

def _jupyter_notebook(notebook_dir=None, port=None, in_tmux=True):
    #jupyter notebook --notebook-dir /home/brian/code/ --port=8777 --no-browser
    command = ['jupyter', 'notebook']
    if notebook_dir is not None:
        command += ['--notebook-dir', notebook_dir]
    if port is not None:
        command += ['--port', str(port)]
    command += ['--no-browser']
    if in_tmux:
        _run_in_tmux('pylab', command)
    else:
        subprocess.Popen(command)

def _xrandr(target, options):
    subprocess.Popen(['xrandr', '--output', target] + options)

def _set_bg(bgpath):
    subprocess.Popen(['feh', '--bg-scale', bgpath])

def _output(*strings, prompt=">>"):
    logger.info(" ".join(strings), extra={'prompt': prompt})

def _single_arg(name, args):
    args = args.split(" ")
    assert len(args) == 1, name + " only accepts single arguments"
    return args[0]

def _scrot(name):
    subprocess.Popen(['scrot', '-s', os.path.join(SCREENSHOTDIR, name+'.png')]).wait()

def _xinput(device_id, property_id, value):
    subprocess.Popen(['xinput', 'set-prop', device_id, property_id, value])

def _get_named_xinput(name):
    config = settings.get_config()
    if 'xinput' not in config:
        print("NO XINPUT IN CONFIG")

class WizardShell(cmd.Cmd):
    intro = "Hello Brian. What would you like to do?"
    prompt = "(wzrd) >> "
    file = None
    #server = libtmux.Server()

    def do_exit(self, args):
        sys.exit(0)

    def do_echo(self, args):
        _output(args)

    def do_scrot(self, args):
        _scrot(_single_arg('scrot', args))

    def do_pylab(self, arg):
        if len(arg) > 0:
            raise NotImplemented("- only local pylab")
        _run_in_tmux("pylab", "~/inky_functions/start_jupyter.sh")

    def do_i3env(self, args):
        arg = _single_arg("i3env", args)

        if arg == "ls":
            files = glob.glob(os.path.join(I3DIR, "config_*"))
            files = [os.path.split(file)[-1] for file in files]
            _output(", ".join(files), prompt="options")
        else:
            _gen_i3_config(arg)

    def do_screens(self, args):
        arg = _single_arg("screens", args)
        if arg == 'ls':
            _output(", ".join(screen_configs.keys()), prompt='options')
        elif arg not in screen_configs:
            raise ValueError(arg + " not in screen configs")
        else:
            for target, options in screen_configs[arg]:
                _xrandr(target, options)

    def do_bg(self, args):
        arg = _single_arg("bg", args)

        if arg == "ls":
            _output(", ".join(bgs.keys()), prompt='options')
        elif arg == "random":
            import random
            _set_bg(random.choice(all_bg))
        elif arg == 'none':
            print("NOT IMPLEMENTED")
        elif arg not in bgs:
            raise ValueError(arg + " not in available backgrounds")
        else:
            _set_bg(bgs[arg])

    def do_xinput(self, args):
        args = args.split(" ")
        if args[0] == 'set':
            name = args[1]
            device_id = args[2]
            prop_id = args[3]

        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("NAME")
        parser.add_argument("id", type=int)
        print(parser.parse_args(args))

    def precmd(self, line):
        return line


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cmd", metavar="cmd", type=str, nargs="+")
    args = parser.parse_args()
    wsh = WizardShell()

    if args.cmd:
        wsh.onecmd(" ".join(args.cmd))
    else:
        WizardShell().cmdloop()

if __name__ == "__main__":
    main()
