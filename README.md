https://www.pygame.org/docs/tut/newbieguide.html

https://www.pygame.org/docs/ref/mask.html

https://www.pygame.org/docs/ref/surface.html#pygame.Surface.get_rect

GAMES: https://www.pygame.org/tags/all




BOIDS: http://www.cs.unc.edu/%7Ehelser/239/finalproj/239_final_paper.htm

>> coding train : https://www.youtube.com/watch?v=mhjuuHl6qHM&t=5s















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


### INSTALLING

>> DEPRECATED!!

```sh
sudo apt-get install -y git pip
git clone https://github.com/PlebeiusGaragicus/arcade-game-menu.git
git clone https://github.com/PlebeiusGaragicus/arcade-apps.git
cd arcade-game-menu
pip install .
```


### MOVING GAMES

```sh
scp 
```


### TODO

- 
- "backend" password-protected python web interface that will allow
