The folders you see at the root of a Linux computer and what they are for.
You do not need to memorise them all; knowing where to look is enough.

| Folder | What is inside | What you do |
|---|---|---|
| `/` | The root; the start of everything | You look |
| `/home` | The users' home folders | You work in your own folder |
| `/home/ada` (`~`) | Your files and settings | Everything |
| `/etc` | The system's settings files (`hostname`, `passwd`) | You read; changing them is an admin job |
| `/tmp` | Temporary files | You can put test files there; they do not stay |
| `/usr` | Installed programs and libraries | You look |
| `/bin`, `/usr/bin` | The commands themselves (`ls`, `cat`, `grep`) | You run them |
| `/var` | Changing data; logs under `/var/log` | You read the logs |
| `/root` | The administrator's (root's) home folder | You cannot go in |

## The Windows equivalents

| Linux | Similar on Windows |
|---|---|
| `/home/ada` | `C:\Users\ada` |
| `/usr/bin` | `C:\Program Files` |
| `/etc` | The registry and settings under `C:\Windows` |
| `/tmp` | `C:\Users\ada\AppData\Local\Temp` |

## In Git Bash

The `/` folder in Git Bash is the folder where Git is installed
(`C:\Program Files\Git`); your Windows disks appear as `/c`, `/d`. Your home
folder is `/c/Users/yourname`.
