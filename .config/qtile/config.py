import os
import subprocess

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal


mod = "mod4"
terminal = guess_terminal()

colors = [
    "003b4c",  # Background
    "66a5ad",  # Current group
    "ececec",  # Highlight Text
    "999999",  # Dark Text
    "73b8bf",  # Widget 1 Color
    "50a5af",  # Widget 2 Color
    "40848c",  # Widget 3 Color
    "306369",  # Widget 4 Color
    "204246",  # Widget 5 Color
    "102123",  # Widget 6 Color
]
fgcolor = colors[0]

catppuccin = {
    "flamingo": "#F3CDCD",
    "mauve": "#DDB6F2",
    "pink": "#f5c2e7",
    "maroon": "#e8a2af",
    "red": "#f28fad",
    "peach": "#f8bd96",
    "yellow": "#fae3b0",
    "green": "#abe9b3",
    "teal": "#b4e8e0",
    "blue": "#96cdfb",
    "sky": "#89dceb",
    "white": "#d9e0ee",
    "gray": "#6e6c7e",
    "black": "#1a1826",
}


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
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
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Rofi config
    Key(["mod4"], "space", lazy.spawn("rofi -show drun")),
    Key(["mod4"], "e", lazy.spawn("nautilus")),
    # Screens
    # Change to other screen
    Key([mod], "u", lazy.to_screen(0)),
    Key([mod], "i", lazy.to_screen(1)),
    # Change the volume if our keyboard has keys
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 -q set Master 2dB+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 -q set Master 2dB-")),
    Key([], "XF86AudioMute", lazy.spawn("amixer -D pulse set Master 1+ toggle")),
    # Commands to control spt spotify player
    Key(
        [],
        "XF86AudioPlay",
        lazy.spawn("spt playback -t"),
        desc="Play/pause music on spt (Spotify)",
    ),
    Key(
        [],
        "XF86AudioPrev",
        lazy.spawn("spt playback -p"),
        desc="Play previous song on spt (Spotify)",
    ),
    Key(
        [],
        "XF86AudioNext",
        lazy.spawn("spt playback -n"),
        desc="Play next song on spt (Spotify)",
    ),
    # Change screen brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 10")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 10")),
]

# Groups -----------------

# groups = [Group(i) for i in "qwertyuiop"]
#
# for i in groups[:-1]:
#    keys.extend(
#        [
#            # mod1 + letter of group = switch to group
#            Key(
#                [mod],
#                i.name,
#                lazy.group[i.name].toscreen(),
#                desc="Switch to group {}".format(i.name),
#            ),
#            # mod1 + shift + letter of group = switch to & move focused window to group
#            Key(
#                [mod, "shift"],
#                i.name,
#                lazy.window.togroup(i.name, switch_group=True),
#                desc="Switch to & move focused window to group {}".format(i.name),
#            ),
#            # Or, use below if you prefer not to switch to that group.
#            # # mod1 + shift + letter of group = move focused window to group
#            # Key([mod, "shift"], i.name, lazy.o group {}".format(i.name)),
#        ]
#    )


def_layout = "bsp"
group_names = [
    ("  ", {"layout": def_layout, "spawn": "alacritty"}),
    ("  ", {"layout": def_layout}),
    ("  ", {"layout": def_layout, "spawn": "google-chrome"}),
    ("  ", {"layout": def_layout}),
    ("  ", {"layout": def_layout}),
    ("  ", {"layout": def_layout}),
    ("  ", {"layout": def_layout}),
    ("  ", {"layout": def_layout}),
    ("  ", {"layout": def_layout, "spawn": "spotify"}),
]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(
        Key([mod], str(i), lazy.group[name].toscreen())
    )  # Switch to another group
    keys.append(
        Key([mod, "shift"], str(i), lazy.window.togroup(name))
    )  # Send current window to another group

# -------------------- Groups


layout_theme = {
    "border_width": 2,
    "margin": 8,
    #"border_focus_stack": ["#d75f5f", "#8f3d3d"],
    "border_focus": catppuccin["green"],
    "border_normal": catppuccin["teal"],
}

layouts = [
    layout.Bsp(**layout_theme),
    layout.Max(**layout_theme),
    # layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    # layout.Columns(),
    # layout.Matrix(),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font",
    fontsize=18,
    padding=6,
    #forground=catppuccin["black"],
)
extension_defaults = widget_defaults.copy()


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth=0,
                    padding=9,
                ),
                widget.GroupBox(
                    rounded=False,
                    active=catppuccin["flamingo"],  # Color of text of active group
                    inactive=catppuccin["green"],
                    highlight_method="line",
                    highlight_color=[catppuccin["black"]],
                    borderwidth=1,
                    this_current_screen_border=catppuccin["flamingo"],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=20,
                ),
                widget.Spacer(),
                widget.TextBox(
                    " Layout:",
                    background=colors[5],
                    foreground=fgcolor,
                ),
                widget.CurrentLayoutIcon(
                    background=colors[5],
                    foreground=fgcolor,
                    scale=0.7,
                    padding=8,
                ),
                #                widget.CurrentLayout(
                #                    background = colors[5],
                #                    foreground = fgcolor,
                #                    padding = 5,
                #                    ),
                widget.Volume(
                    emoji=False,
                    background=colors[6],
                    foreground=fgcolor,
                    fmt=" {}",
                    padding=8,
                ),
                widget.Clock(
                    format=" %d/%m/%y  %H:%M",
                    background=colors[7],
                    foreground=fgcolor,
                    padding=9,
                ),
                widget.Battery(
                    background=colors[8],
                    foreground=fgcolor,
                    format=" {char} {percent:2.0%} {hour:d}:{min:02d}",
                    padding=9,
                ),
            ],
            24,
            margin=[4, 6, 1, 6],
            opacity=0.85,
            background=catppuccin["black"],
        ),
        bottom=bar.Bar(
            [
                widget.Prompt(),
                widget.WindowName(),
                widget.CheckUpdates(
                    distro="Arch",
                    fmt=" - {}",
                    background=colors[5],
                    foreground=fgcolor,
                    padding=9,
                    no_update_string=" : N/A",
                ),
                widget.Pomodoro(
                    background=colors[6],
                    foreground=fgcolor,
                    padding=9,
                    color_inactive="ff9933",
                ),
                # widget.HDDGraph(
                #     background = colors[7],
                #     foreground = fgcolor,
                #     path = '/dev/sda2',
                #     ),
                widget.Systray(),
            ],
            26,
            margin=[1, 6, 4, 6],
            opacity=0.85,
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth=0,
                    padding=9,
                ),
                widget.GroupBox(
                    rounded=False,
                    active=colors[7],  # Color of text of active group
                    inactive=colors[6],
                    highlight_method="block",
                    highlight_color=[colors[3], colors[4]],
                    # current_screen_border = colors[1],
                    this_current_screen_border=colors[1],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=20,
                ),
                widget.Spacer(),
                widget.TextBox(
                    " Layout:",
                    background=colors[5],
                    foreground=fgcolor,
                ),
                widget.CurrentLayoutIcon(
                    background=colors[5],
                    foreground=fgcolor,
                    scale=0.7,
                    padding=8,
                ),
                #                widget.CurrentLayout(
                #                    background = colors[5],
                #                    foreground = fgcolor,
                #                    padding = 5,
                #                    ),
                widget.Volume(
                    emoji=False,
                    background=colors[6],
                    foreground=fgcolor,
                    fmt=" {}",
                    padding=8,
                ),
                widget.Clock(
                    format=" %d/%m/%y  %H:%M",
                    background=colors[7],
                    foreground=fgcolor,
                    padding=9,
                ),
                widget.Battery(
                    background=colors[8],
                    foreground=fgcolor,
                    format=" {char} {percent:2.0%} {hour:d}:{min:02d}",
                    padding=9,
                ),
            ],
            24,
            margin=[4, 6, 1, 6],
            opacity=0.85,
        ),
        bottom=bar.Bar(
            [
                widget.Prompt(),
                widget.WindowName(),
                widget.CheckUpdates(
                    distro="Arch",
                    fmt=" - {}",
                    background=colors[5],
                    foreground=fgcolor,
                    padding=9,
                    no_update_string=" : N/A",
                ),
                widget.Pomodoro(
                    background=colors[6],
                    foreground=fgcolor,
                    padding=9,
                    color_inactive="ff9933",
                ),
                # widget.HDDGraph(
                #     background = colors[7],
                #     foreground = fgcolor,
                #     path = '/dev/sda2',
                #     ),
                widget.Systray(),
            ],
            26,
            margin=[1, 6, 4, 6],
            opacity=0.85,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
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


# Hooks
@hook.subscribe.startup_once
def start_once():
    start_script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.call([start_script])
