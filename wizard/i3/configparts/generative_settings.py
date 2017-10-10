basic_order = [
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
orders = {
    'office': basic_order + ['officebar-config'],
    'mobile': basic_order + ['mobilebar-config']
}

workspaces = {
}
