import os

from wizard.i3 import settings as i3settings
from wizard import settings as wizsettings
import shutil

def get_config(version='mobile', generate_workspace_config=True):
    files = i3settings.config_files[version]

    intermediate = '\n' * 2 + '#+' * 40 + '\n' * 2

    final_config = []

    for f in files:
        if generate_workspace_config and f == 'workspace-config':
            conf_data = make_workspace_config()
        else:
            with open(os.path.join(i3settings.HERE, 'configparts', f)) as fp:
                conf_data = fp.read()

        if f == 'header-config':
            conf_data = conf_data.format(monitor_name=i3settings.MOBILE_MONITOR)

        final_config.append(conf_data)

    final_config = intermediate.join(final_config)

    return final_config


def make_workspace_config(mod_key=i3settings.MOD_KEY):
    set_name_vars = []
    set_key_vars = []
    rename_workspaces = []
    bindsyms = []
    bindsym_moves = []


    for index, workspace in enumerate(i3settings.workspaces, 1):
        name = workspace['name']
        key = workspace['key']
        w_var = f"{mod_key}w{index}"
        k_var = f"{mod_key}b{index}"
        set_name_vars.append(f"set {w_var} {name}")
        set_key_vars.append(f"set {k_var} {key}")
        rename_workspaces.append(f"exec rename workspace {index} to {w_var}")
        bindsyms.append(f"bindsym {mod_key}+{k_var} workspace {w_var}")

        bindsym_moves.append(f"bindsym mod1+{k_var} move container to "
                             f"workspace {w_var}; mode \"default\"")

    out = f"bindsym {mod_key}+Control+Right move workspace to output right\n"
    out += f"bindsym {mod_key}+Control+Left move workspace to output left\n"
    out += f"bindsym {mod_key}+Control+Up move workspace to output up\n"
    out += f"bindsym {mod_key}+Control+Down move workspace to output down\n"

    out += "\n".join(set_name_vars)
    out += '\n' * 3
    out += "\n".join(set_key_vars)
    out += '\n' * 3
    out += "\n".join(rename_workspaces)
    out += '\n' * 3
    out += "\n".join(bindsyms)
    out += '\n' * 3

    out += "bindsym mod1+space mode \"move container\"\n"
    out += '\n' * 3
    out += "mode \"move container\" {\n"
    out += "\n".join([" "*8 + b for b in bindsym_moves])

    out += " "*8 + "bindsym Return mode \"default\"\n"
    out += " "*8 + "bindsym Escape mode \"default\"\n"

    out += "}"

    return out


def copy_config(version='mobile'):
    config = get_config(version)
    with open(os.path.join(wizsettings.I3DIR, 'config'), 'w') as fp:
        fp.write(config)

    files = ['memory', 'battery', 'battery2', 'disk', 'cpu_usage', 'volume',
             'mobile_bottom.conf', 'mobile_top.conf', 'iface', 'wifi']
    for f in files:

        from_path = os.path.join(i3settings.HERE, 'cache', f)
        to_path = os.path.join(wizsettings.I3DIR, f)

        shutil.copyfile(from_path, to_path)
