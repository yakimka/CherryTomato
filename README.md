# CherryTomato 🍅

Easy-to-use, flexible Pomodoro Technique timer built with PyQt5.

[![build](https://github.com/yakimka/CherryTomato/workflows/build/badge.svg)](https://github.com/yakimka/CherryTomato/actions?query=workflow:build)
[![codecov](https://codecov.io/gh/yakimka/CherryTomato/branch/master/graph/badge.svg)](https://codecov.io/gh/yakimka/CherryTomato)

![Screenshot](https://github.com/yakimka/CherryTomato/raw/master/assets/screenshot.png)

## 🌟 Features

- **Simple Interface:** Get started with Pomodoro Technique in seconds.
- **Configurable Intervals:** Tailor the timer to your needs.
- **Notifications:** Know instantly when an interval ends.
- **Short & Long Breaks:** Based on your progress.
- **Tomato Tracker:** Keep count of your productivity.
- **Switch State:** Quick toggle between tomato and break.
- **Event Driven Commands:** Execute custom scripts on timer events.

## 📋 Requirements

- Python (>= 3.6)
- PyQt5

## ✅ Tested On

- Arch Linux
- KDE5
- Xorg X server | Wayland session
- FullHD Display
- Python versions: 3.7, 3.8, 3.9

## 🔧 Installation

### Using pip

```bash
pip install --user CherryTomato
```

After installation, run `cherry_tomato` in the terminal. Ensure `~/.local/bin` is in your PATH.

To add CherryTomato to your application launcher:
1. Create a `.desktop` file at `~/.local/share/applications/cherrytomato.desktop`.
2. Add the following content (replace `USER` and `VERSION` accordingly):

```plaintext
[Desktop Entry]
Type=Application
Name=CherryTomato
GenericName=Easy to use, flexible PyQt5 Pomodoro Technique timer
Icon=/home/USER/.local/lib/pythonVERSION/site-packages/CherryTomato/media/icon.png
Exec=$HOME/.local/bin/cherry_tomato
Terminal=false
Categories=Utility
```

### For Arch Linux Users

Install from the AUR:

```bash
yaourt -S cherrytomato
```

Or, [Visit CherryTomato on AUR](https://aur.archlinux.org/packages/cherrytomato)

## 💡 Execute Custom Commands

CherryTomato allows the execution of custom commands during certain timer events. 

❗ **Note:** Any process initiated by these commands won't terminate automatically upon CherryTomato's exit.

Timer details can be passed to your scripts using macros:

- `{tomatoes}` - Number of completed tomatoes.
- `{state}` - Current timer state ("tomato", "break", or "long_break").

### Examples

You can write a script and use it with CherryTomato:

```shell script
#!/bin/bash

tomatoes=$1
state=$2

if [ $tomatoes -gt 10 ]
then
    # ...
    # greater than 10 logic
    # ...
else
    # ...
    # lesser than 11 logic
    # ...
fi


if [ $state = "tomato" ]
then
    # ...
    # is tomato state logic
    # ...
elif [ $state = "break" ]
then
    # ...
    # is break state logic
    # ...
elif [ $state = "long_break" ]
then
    # ...
    # is long break state logic
    # ...
fi
```

Another examples:

- You can play and pause music on Spotify with commands:

    `dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Play`
    
    `dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause`

- You can send messages to your phone with KDE Connect:
    
    `kdeconnect-cli --ping-msg "It's Tomato Time!" -n "Phone name"`

## 🔍 Troubleshooting

- **Problem with Tomato Icon?** See this [issue thread](https://github.com/yakimka/CherryTomato/issues/13).

## 📜 Credits

- Icons: Courtesy of [Freepik](https://www.flaticon.com/authors/freepik) from [Flaticon](www.flaticon.com).
- Notification Sound: ["Notification Sound"](https://freesound.org/people/rhodesmas/sounds/342755/) by rhodesmas under CC BY 3.0.
