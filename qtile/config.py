# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
# Copyright (c) 2024 Florine0928
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

from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.dgroups import simple_key_binder
from libqtile.widget import backlight
from libqtile import hook
import subprocess

@hook.subscribe.startup
def startup():
    subprocess.run(["gomgr", "-r", "wallpaper"])

mod = "mod4"
terminal = guess_terminal() # or kitty

keys = [
    Key([mod], "q", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "b", lazy.spawn("blueman-manager")),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "space", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod], "m", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("sh -c 'GTK_THEME=Gruvbox-Dark wofi --show drun'")),
    Key(["shift"], "Print", lazy.spawn("bash -c '~/.config/Scripts/screenshot-grim-selection.sh'")),
    Key([], "Print", lazy.spawn("bash -c '~/.config/Scripts/screenshot-grim.sh'")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 5%-"), desc="Lower Volume by 5%"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 5%+"), desc="Raise Volume by 5%"),
    Key([], "XF86AudioMute", lazy.spawn("amixer sset Master 1+ toggle"), desc="Mute/Unmute Volume"), 
]

for vt in range(1, 8):
    keys.append(Key(["control", "mod1"],f"f{vt}",lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),))

groups = [
    Group(""),
    Group(""),
    Group(""),
    Group(""),
    Group("󰝚"),
    Group("󰉋"),
    Group("󰊢"),
    Group(""),
    Group(""),
]

layout_theme = {"border_width": 2,"margin": 8,"border_focus": "#fabd2f","border_normal": "689d6a"}
floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class='confirmreset'),
        Match(wm_class='blueman-manager'),
    ]
)
layouts = [
    layout.Columns(border_width=1, margin=1,margin_on_single=6, border_focus="#fabd2f", border_normal="928375", border_on_single=True),
    layout.Floating(**layout_theme),
]

widget_defaults = dict(
    font="FiraCode Nerd Font Bold",
    foreground="#ebdbb2",
    background="#1d2021",
    fontsize=12,
    padding=8,
    active="ebdbb2", # GroupBox Param
    block_highlight_text_color="#fabd2f", # GroupBox Param
    highlight_color="#fabd2f", # GroupBox Param
    inactive="928374", # GroupBox Param
    this_current_screen_border="#fabd2f", # GroupBox Param, fucks sake! I scrambled to find this garbage, why is it so esoteric?
                                          # for a fucking simple thing as hightlight color for workspace, should've just been activeworkspace_highlight...
    highlight_method='text', # GroupBox Param
) 

extension_defaults = widget_defaults.copy()

screens = [Screen(top=bar.Bar([
                widget.GroupBox(fontsize=20),
                widget.WindowName(max_chars=50),
                widget.StatusNotifier(),
                widget.Systray(),
                widget.Bluetooth(),
                widget.Sep(size_percent=50),
                widget.TextBox(text="",fontsize=18),
                widget.Memory(format='{MemUsed: .0f}{mm}'),
                widget.Sep(size_percent=50),
                widget.TextBox(text="",fontsize=18),
                widget.CPU(format='{load_percent}%'),
                widget.Sep(size_percent=50),
                widget.TextBox(text="󰃰",fontsize=18),
                widget.Clock(format="%Y/%m/%d %a %I:%M %p"),],35,background="#282828",
                border_width=[0, 0, 2, 0],  # Draw top and bottom borders
                border_color=["#fabd2f", "#fabd2f", "#fabd2f", "#fabd2f"]  # Borders are magenta
        ),),]
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = simple_key_binder("mod4")
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

auto_minimize = True
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose FlorinWM to maximize irony: it is a non existant WM
wmname = "FlorinWM"
