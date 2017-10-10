import os
import glob

I3DIR = os.path.join(os.environ['HOME'], '.config/i3')
BGDIR = os.path.join(os.environ['HOME'], 'Pictures/wallpapers')
SCREENSHOTDIR = os.path.join(os.environ['HOME'], 'Pictures/screenshots')

def assert_exists(some_dir):
    if not os.path.exists(some_dir):
        os.makedir(some_dir)

assert_exists(SCREENSHOTDIR)
assert_exists(BGDIR)

screen_configs = {'office': [('HDMI-0', ['--auto', '--primary']),
                             ('eDP-1-1', ['--off'])],
                  'mobile': [('HDMI-0', ['--off']),
                             ('eDP-1-1', ['--auto', '--primary'])]}

bgs = {'gnu': os.path.join(BGDIR, 'minimalistdump_fromreddit/gnu.png')}

all_bg = glob.glob(os.path.join(BGDIR, "*.png"))
all_bg += glob.glob(os.path.join(BGDIR, "*.jpg"))
all_bg += glob.glob(os.path.join(BGDIR, "*/*.png"))
all_bg += glob.glob(os.path.join(BGDIR, "*/*.jpg"))
