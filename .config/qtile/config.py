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

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import PulseVolume
import os
import subprocess
import datetime

mod = "mod4"
terminal = guess_terminal()


# --------startup-------#

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/start.sh'])


# ------end-startup-----#
	
# -----------keys----------#
keys = [
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
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
    # ----------my keybins-----------#
    Key([mod, "shift"], "f", lazy.spawn("firefox-developer-edition"), desc="Launch firefox"),
    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +10%"), desc="+10 volume"),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -10%"),desc="-1' volume"),
    Key([], "Print",
        lazy.spawn("python3 /home/fabri/.config/qtile/screenshot.py && notify-send 'screenshot taked'")),
    Key([mod], "t", lazy.spawn("pcmanfm"), desc="Lauch pcmanfm"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="Launch launcher"),
]
# groups = [Group(i) for i in "123456789"]
# ---------workspaces--------------#
groups = [
    Group(name="1", label="  ", layout="monadtall",
          matches=[
              Match(wm_class="tilix"),
              Match(wm_class="Alacritty"),
              Match(wm_class="Termite"),
              Match(wm_class="Xfce4-terminal"),
          ]),
    Group(name="2", label="  ", layout="monadtall",
          matches=[
              Match(wm_class="google-chrome-stable"),
              Match(wm_class="firefoxdeveloperedition"),
              Match(wm_class="Vivaldi-stable"),
          ]),
    Group(name="3", label="  ", layout="monadtall",
          matches=[
              Match(wm_class="Org.gnome.Nautilus"),
          ]),
    Group(name="4", label="", layout="monadtall",
          matches=[
              Match(wm_class="discord"),
          ]),
    Group(name="5", label="  ", layout="monadtall",
          matches=[
              Match(wm_class="Sublime_text"),
          ]),
    Group(name="6", label="  ", layout="monadtall",
          matches=[
              Match(wm_class="RStudio"),
          ]),
    Group(name="7", label="  ", layout="monadtall",
          matches=[
              Match(wm_class="Typora"),
              Match(wm_class="zettlr"),
              Match(wm_class="marktext"),
          ]),
    Group(name="8", label="", layout="monadtall",
          matches=[
              Match(wm_class="Lxappearance"),
	      Match(wm_class="Spotify"),
          ]),
]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layoutTheme = {"border_focus": "#7730B3",
               "border-width": 2,
               "margin": 22,
	       "border_normal":"#A461BE",
               "font": "Hack"
               }
layouts = [
    layout.Columns(**layoutTheme),
    layout.Tile(**layoutTheme),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

Cbackground = "#282a36"

color = [
    ["#424153", "#424153"],  # dark
    ["4c175f", "4c175f"],  # violet
    ["#993399", "#993399"],  # pink dark
    ["333399", "333399"],  # blue
    ["ea4c88", "ea4c88"],  # pink
    ["#FFFFFF", "#FFFFFF"],  # white
]
# ------------bar---------#
screens = [
    Screen(
        bottom=bar.Bar(
            [
		widget.GroupBox(background=color[1], foreground=color[5]),
                widget.Prompt(background=color[4], foreground=color[0]),
                #widget.WindowName(background=color[0], foreground=color[4], opacity=0.1),
		widget.Spacer(background="#00000000", opacity=1),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # widget.TextBox("default config", name="default"),
                # widget.TextBox("Press &lt;M-r&gt; to spawn",
                # foreground="#d75f5f"),
                #widget.CurrentLayout(background="#00000000", foreground=color[4]),
                #widget.Systray(background=color[1], foreground=color[4], opacity=0),
		#widget.Systray(backgrond="#00000000"),
		widget.TextBox("",background=color[1]),
		widget.Volume(background=color[1]),
                widget.Clock(format='%d/%m/%y %H:%M:%S',
                             background=color[1], opacity=0),

                #widget.QuickExit(background=color[1], foreground=color[0]),
            ],
            24,
	    background="#00000000",
	    opacity=1,
        ),
    ),
]
# ----------end-bar--------#

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
