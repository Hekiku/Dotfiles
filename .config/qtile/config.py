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

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import subprocess
import os
from libqtile import hook

from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration


@hook.subscribe.startup
def dbus_register():
    id = os.environ.get('DESKTOP_AUTOSTART_ID')
    if not id:
        return
    subprocess.Popen(['dbus-send',
                      '--session',
                      '--print-reply',
                      '--dest=org.gnome.SessionManager',
                      '/org/gnome/SessionManager',
                      'org.gnome.SessionManager.RegisterClient',
                      'string:qtile',
                      'string:' + id])


mod = "mod4"		    # Mod key to SUPER/WINDOWS
terminal = "alacritty"  # My terminal of choice
browser = "firefox"	    # My browser of choice

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    # Essentials
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "n", lazy.spawn("google-chrome"), desc="Launch google chrome"),
    Key([mod], "m", lazy.spawn("telegram-desktop"), desc="Launch telegram"),
    # Qtile control
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Control Audio
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "amixer sset Master 5%-"), desc="Lower Volume by 5%"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "amixer sset Master 5%+"), desc="Raise Volume by 5%"),
    Key([], "XF86AudioMute", lazy.spawn(
        "amixer sset Master 1+ toggle"), desc="Mute/Unmute Volume"),
    # Screenshot
    Key([], "Print", lazy.spawn('gnome-screenshot -i'), desc="Launch screenshot"),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(
                    i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.MonadTall(),
    layout.Spiral(ratio=0.5, new_client_position="bottom"),
    layout.Columns(),
    layout.Max()
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

colors = [["#282c34", "#282c34"],
          ["#1c1f24", "#1c1f24"],
          ["#dfdfdf", "#dfdfdf"],
          ["#ff6c6b", "#ff6c6b"],
          ["#98be65", "#98be65"],
          ["#da8548", "#da8548"],
          ["#51afef", "#51afef"],
          ["#c678dd", "#c678dd"],
          ["#46d9ff", "#46d9ff"],
          ["#a9a1e1", "#a9a1e1"]]

widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize=10,
    padding=2,
    background="#dfdfdf"
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper='/usr/share/backgrounds/Startrail_by_Hajime_Mizuno.jpg',
        wallpaper_mode='fill',
        bottom=bar.Bar(
            [
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    foreground=colors[2],
                    background=colors[0]
                ),
                widget.GroupBox(
                    font="Ubuntu Bold",
                    fontsize=9,
                    margin_y=3,
                    margin_x=0,
                    padding_y=3,
                    padding_x=3,
                    borderwidth=3,
                    active=colors[2],
                    inactive=colors[7],
                    rounded=False,
                    highlight_color=colors[1],
                    highlight_method="line",
                    this_current_screen_border=colors[6],
                    this_screen_border=colors[4],
                    other_current_screen_border=colors[6],
                    other_screen_border=colors[4],
                    foreground=colors[2],
                    background=colors[0]
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    foreground=colors[2],
                    background=colors[0]
                ),
                widget.TextBox(
                    text='|',
                    font="Ubuntu Mono",
                    background=colors[0],
                    foreground='474747',
                    padding=2,
                    fontsize=14
                ),
                widget.CurrentLayoutIcon(
                    custom_icon_paths=[os.path.expanduser(
                        "~/.config/qtile/icons")],
                    foreground=colors[2],
                    background=colors[0],
                    padding=0,
                    scale=0.7
                ),
                widget.CurrentLayout(
                    foreground=colors[2],
                    background=colors[0],
                    padding=5
                ),
                widget.TextBox(
                    text='|',
                    font="Ubuntu Mono",
                    background=colors[0],
                    foreground='474747',
                    padding=2,
                    fontsize=14
                ),
                widget.WindowName(
                    foreground=colors[6],
                    background=colors[0],
                    padding=0
                ),
                widget.Prompt(
                    foreground=colors[6],
                    background=colors[0],
                    padding=0),
                widget.Systray(
                    background=colors[0],
                    padding=5
                ),
                # widget.Sep(
                #     linewidth = 0,
                #     padding = 6,
                #     foreground = colors[0],
                #     background = colors[0]
                # ),
                # widget.CheckUpdates(
                #     update_interval = 1800,
                #     custom_command="apt list --upgradable",
                #     display_format = "Updates: {updates} ",
                #     no_update_string = 'No updates',
                #     mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('alacritty -e apt list --upgradable')},
                #     foreground = colors[5],
                #     colour_have_updates = colors[5],
                #     colour_no_updates = colors[5],
                #     padding = 5,
                #     background = colors[0],
                #     decorations=[
                #         BorderDecoration(
                #             colour = colors[5],
                #             border_width = [0, 0, 2, 0],
                #             padding_x = 5,
                #             padding_y = None,
                #         )
                #     ],
                # ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    foreground=colors[0],
                    background=colors[0]
                ),
                widget.Wlan(
                    foreground=colors[4],
                    background=colors[0],
                    padding=5,
                    decorations=[
                        BorderDecoration(
                            colour=colors[4],
                            border_width=[0, 0, 2, 0],
                            padding_x=5,
                            padding_y=None,
                        )
                    ],
                    interface='wlp4s0',
                    format='{essid} {percent:2.0%}'
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    foreground=colors[0],
                    background=colors[0]
                ),
                widget.Volume(
                    foreground=colors[7],
                    background=colors[0],
                    fmt='Vol: {}',
                    padding=5,
                    decorations=[
                        BorderDecoration(
                            colour=colors[7],
                            border_width=[0, 0, 2, 0],
                            padding_x=5,
                            padding_y=None,
                        )
                    ],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    foreground=colors[0],
                    background=colors[0]
                ),
                widget.KeyboardLayout(
                    foreground=colors[8],
                    background=colors[0],
                    fmt='Keyboard: {}',
                    padding=5,
                    decorations=[
                        BorderDecoration(
                            colour=colors[8],
                            border_width=[0, 0, 2, 0],
                            padding_x=5,
                            padding_y=None,
                        )
                    ],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    foreground=colors[0],
                    background=colors[0]
                ),
                widget.Clock(
                    foreground=colors[6],
                    background=colors[0],
                    format="%A, %d %B %Y - %H:%M ",
                    decorations=[
                        BorderDecoration(
                            colour=colors[6],
                            border_width=[0, 0, 2, 0],
                            padding_x=5,
                            padding_y=None,
                        )
                    ],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    foreground=colors[0],
                    background=colors[0]
                ),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
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

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
