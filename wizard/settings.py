import os
import glob
import configparser

I3DIR = os.path.join(os.environ['HOME'], '.config/i3')
BGDIR = os.path.join(os.environ['HOME'], 'Pictures/wallpapers')
WIZDIR = os.path.join(os.environ['HOME'], '.wizard')
SCREENSHOTDIR = os.path.join(os.environ['HOME'], 'Pictures/screenshots')

def assert_exists(some_dir):
    if not os.path.exists(some_dir):
        os.makedir(some_dir)

assert_exists(SCREENSHOTDIR)
assert_exists(BGDIR)
assert_exists(WIZDIR)

screen_configs = {'office': [('HDMI-0', ['--auto', '--primary']),
                             ('eDP-1-1', ['--off'])],
                  'mobile': [('HDMI-0', ['--off']),
                             ('eDP-1-1', ['--auto', '--primary'])]}

bgs = {'gnu': os.path.join(BGDIR, 'minimalistdump_fromreddit/gnu.png')}

all_bg = glob.glob(os.path.join(BGDIR, "*.png"))
all_bg += glob.glob(os.path.join(BGDIR, "*.jpg"))
all_bg += glob.glob(os.path.join(BGDIR, "*/*.png"))
all_bg += glob.glob(os.path.join(BGDIR, "*/*.jpg"))

HERE = dir_path = os.path.dirname(os.path.realpath(__file__))

DEFAULT_INI='settings.ini'

def get_config(ini_filename=DEFAULT_INI):
    if WIZDIR not in ini_filename:
        ini_filename = os.path.join(WIZDIR, ini_filename)
    if not os.path.exists():
        with open(ini_filename, 'a'):
            pass

    config = configparser.ConfigParser()
    config.read(ini_filename)
    return config

def set_config_value(name, value, section='default', ini_filename=DEFAULT_INI):
    ini_filename = os.path.join(WIZDIR, ini_filename)
    config = get_config(ini_filename)
    config[section][name] = value
    with open(ini_filename, 'w') as fp:
        config.write(fp)

