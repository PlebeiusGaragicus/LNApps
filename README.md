# LNApps

> trying to run the python application

myca@jupiter LNApps % ./fishy
./fishy: fork: Resource temporarily unavailable
myca@jupiter LNApps % ./fishy
__vsc_command_output_start:2: fork failed: resource temporarily unavailable
zsh: fork failed: resource temporarily unavailable
__vsc_update_cwd:1: fork failed: resource temporarily unavailable    


> running any command in VS Code terminal (it works but shows:)

__vsc_command_output_start:2: fork failed: resource temporarily unavailable

> Opening a new terminal:

[forkpty: Resource temporarily unavailable]
[Could not create a new process and open a pseudo-tty.]

---

# check running processes
ps aux | wc -l

# check for zombie processes
ps aux | grep 'Z'

1. A zombie process will have a 'Z' in the 'STAT' column.

`htop` or `top`

---

appears the cause of the issue is the rsync-sync extension for VS Code

Solution: comment out .vscode/settings.json

Here are the contents for backup:

```json
{
    "sync-rsync.remote": "satoshi@lnarcade.local:/home/satoshi/LNApps/",
    "sync-rsync.onSave": true,
    "sync-rsync.onSaveIndividual": true,
    "sync-rsync.options": [],
    "sync-rsync.sites": [],
    "sync-rsync.notification": false
}
```
