import os

config_file_list = [
    'header-config',
    'basicfunction-config',
    'basicwindow-config',
    'floatingwindow-config',
    'workspace-config',
    'scratchpad-config',
    'frameless-config',
    'gaps-config',
    'layout-config',
    'convenience-config',
]

# office and mobile will differe on bars & monitor info stuff
config_files = {
    'office': config_file_list + ['officebar-config'],
    'mobile': config_file_list + ['mobilebar-config']
}

workspaces = [
    {'name': '[q]ux', 'key': 'q'},
    {'name': '[w]eb', 'key': 'w'},
    {'name': '[e]lb', 'key': 'e'},
    {'name': '[r]es', 'key': 'r'},
    {'name': '[a]xe', 'key': 'a'},
    {'name': '[s]sh', 'key': 's'},
    {'name': '[d]ev', 'key': 'd'},
    {'name': '[f]oo', 'key': 'f'},
    {'name': '[z]oo', 'key': 'z'},
    {'name': '[x]yz', 'key': 'x'},
    {'name': '[c]md', 'key': 'c'},
    {'name': '[v]at', 'key': 'v'},
]

MOD_KEY = '$hyp'

HERE = os.path.dirname(os.path.realpath(__file__))

MOBILE_MONITOR = os.environ['MOBILE_MONITOR']
