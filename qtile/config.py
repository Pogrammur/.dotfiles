# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


########## Imports
##############################
import os
import subprocess
from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy


########## Qtile-Extras Imports
##############################
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration
#from qtile_extras.widget import StatusNotifier
import colors


########## Variables
##############################
mod = "mod4"
terminal = "alacritty"
browser = "firefox"
editor = "nvim"


########## Variables
##############################
# A function for hide/show all the windows in a group
@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()


########## Keys
##############################
keys = [

    ##### The Essentials
    Key([mod], "Return", lazy.spawn(terminal), desc="Terminal"),
    Key([mod], "b", lazy.spawn(browser), desc="Browser"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod],"f", lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",),

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),

    # Switch focus of monitors
    Key([mod], "period", lazy.next_screen(), desc='Move focus to next monitor'),
    Key([mod], "comma", lazy.prev_screen(), desc='Move focus to next monitor'),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


########## Groups
##############################
groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]

group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]
#group_labels = ["DEV", "WWW", "SYS", "DOC", "VBOX", "CHAT", "MUS", "VID", "GFX",]
#group_labels = ["", "", "", "", "", "", "", "", "",]

group_layouts = ["tile", "monadtall", "tile", "tile", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]


for i in range(len(group_names)):
    groups.append(
            Group(
                name=group_names[i],
                layout=group_layouts[i].lower(),
                label=group_labels[i],
            ))

for i in groups:
    keys.extend(
        [
            # mod1 + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

########## Layouts
##############################

colors = colors.DoomOne

layout_theme = {
        "border_width": 3,
        "margin": 8,
        "border_focus": colors[8],
        "border_normal": colors[0],
        }

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Bsp(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    layout.Tile(**layout_theme,
                shift_windows=True,
                ratio = 0.335,
                ),
    # layout.TreeTab(),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme),
]

########## Widgets
##############################
widget_defaults = dict(
    font="lilex",
    fontsize=12,
    padding=0,
    background=colors[0],
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
            widget.Image(
                filename = "~/.config/qtile/icons/arch.jpg",
                scale = "False",
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal)},
                ),
            widget.Prompt(
                font = "lilex",
                fontsize=14,
                foreground = colors[1],
                ),
            widget.GroupBox(
                fontsize = 11,
                margin_y = 5,
                margin_x = 5,
                padding_y = 0,
                padding_x = 1,
                borderwidth = 3,
                active = colors[8],
                inactive = colors[1],
                rounded = False,
                highlight_color = colors[2],
                highlight_method = 'line',
                this_current_screen_border = colors[7],
                this_screen_border = colors[4],
                other_current_screen_border = colors[7],
                other_screen_border = colors[4],
                ),
            widget.TextBox(
                text = '|',
                font = 'lilex',
                foreground = colors[1],
                padding = 2,
                fontsize = 14,
                ),
            widget.CurrentLayoutIcon(
                #custom_icon_paths = [os.path.expanduser('~/.config/qtile/icons')],
                foreground = colors[1],
                padding = 4,
                scale = 0.6,
                ),
            widget.CurrentLayout(
                foreground = colors[1],
                padding = 5,
                ),
            widget.TextBox(
                text = '|',
                font = 'lilex',
                foreground = colors[1],
                padding = 2,
                fontsize = 14,
                ),
            widget.WindowName(
                    foreground = colors[6],
                    max_chars = 40,
                    ),
            widget.GenPollText(
                    update_interval = 300,
                    func = lambda: subprocess.check_output('printf $(uname -r)', shell=True, text=True),
                    foreground = colors[3],
                    fmt = '❤  {}',
                    decorations=[
                        BorderDecoration(
                            colour = colors[3],
                            border_width = [0, 0, 2, 0],
                            )
                        ],
                    ),
#            widget.Spacer(length = 8),
#            widget.CPU(
#                    format = '▓  Cpu: {load_percent}%',
#                    foreground = colors[4],
#                    decorations=[
#                        BorderDecoration(
#                            colour = colors[4],
#                            border_wdith = [0, 0 , 2, 0,],
#                            ),
#                        ],
#                    ),
#            widget.Spacer(length = 8),
#            widget.Memory(
#                foreground = colors[8],
#                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(termial + ' -e htop')},
#                format = '{MemUsed: .0f}{mm}',
#                fmt = '🖥  Mem: {} used',
#                decorations=[
#                    BorderDecoration(
#                        colour = colors[8],
#                        border_width = [0, 0, 2, 0],
#                        )
#                    ],
#                ),
            widget.Spacer(length = 8),
            widget.DF(
                 update_interval = 60,
                 foreground = colors[5],
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e df')},
                 partition = '/',
                 #format = '[{p}] {uf}{m} ({r:.0f}%)',
                 format = '{uf}{m} free',
                 fmt = '🖴  Disk: {}',
                 visible_on_warn = False,
                 decorations=[
                     BorderDecoration(
                         colour = colors[5],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
            widget.Spacer(length = 8),
            widget.KeyboardLayout(
                    foreground = colors[4],
                    fmt = '⌨  Kbd: {}',
                    decorations=[
                        BorderDecoration(
                            colour = colors[4],
                            border_width = [0, 0, 2, 0],
                            ),
                        ],
                    ),

            widget.Spacer(length = 8),
            widget.Clock(
                    foreground = colors[8],
                    format = "⏱  %a, %b %d - %H:%M",
                    decorations=[
                        BorderDecoration(
                            colour = colors[8],
                            border_width = [0, 0, 2, 0],
                            ),
                        ],
                    ),
            widget.Spacer(length = 8),
            widget.Systray(padding = 3),
            widget.Spacer(length = 8),

            ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[22:24]
    return widgets_screen2


########## Screens
##############################

# For adding transparency to your bar, add (background="#00000000") to the "Screen" line(s)
# For ex: Screen(top=bar.Bar(widgets=init_widgets_screen2(), background="#00000000", size=24)),

def init_screens():
    return[Screen(top=bar.Bar(widgets=init_widgets_screen1(), background="#00000000", size=26)),
           Screen(top=bar.Bar(widgets=init_widgets_screen2(), background="#00000000", size=26)),
           Screen(top=bar.Bar(widgets=init_widgets_screen2(), background="#00000000", size=26)),
           ]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

########## Mouse
##############################
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None


########## Hooks
##############################
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
