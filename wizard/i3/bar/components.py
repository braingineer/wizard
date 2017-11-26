
memory = """
[memory]
label=⧖
command=~/.config/i3/memory
interval=30
color=#888888
"""

battery = """
[batterytwo]
label=⚡
command=echo "$(~/.config/i3/battery2)"
interval=10
color=#888888
"""

disk = """
[disk-root]
label=⦿:
command=~/.config/i3/disk /
interval=30
#color=#1793D1
color=#888888
"""

gputemp = """
[gputemp]
label=
command=echo "$(nvidia-smi | awk '/6072MiB/ {print $3}')"
interval=10
#color=#bf8900
#separator=false
color=#888888
"""

cpu = """
[cpu]
label=
command=~/.config/i3/cpu_usage
interval=10
#separator=false
color=#888888
"""

temp = """
[temp]
command=echo "$(sensors coretemp-isa-0000 | awk '/Physical/ {print $4}')"
interval=10
#color=#b58900
color=#888888
"""

volume = """
[volume]
label=
command=~/.config/i3/volume
interval=2
signal=10
#color=#d70a53
color=#888888
"""

time = """
[time]
label=
command=date '+%a %m-%d-%y %l:%M:%S %p'
interval=5
color=#888888
"""

memory2 = """
[memory]
command=echo RAM [ $(~/.config/i3/memory) ]
interval=10
color=#b58900
min_width=50
align=left
"""

sep = """
[separator]
"""

gpuuse = """
[gpuuse]
command=echo "$(nvidia-smi | awk '/6072MiB/ {print $9}') / 6072 MiB ]"
interval=10
color=#bf8900
min_width=50
align=left
"""
