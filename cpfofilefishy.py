#!/usr/bin/env python3

import cProfile

from fishyfrens.app import App

parameters = """
Sorting Options:
'calls': Sort by the number of calls to the function.
'cumtime': Sort by cumulative time spent in the function and its sub-functions.
'file': Sort by the file name the function was defined in.
'line': Sort by the line number the function was defined at.
'module': Sort by the module name.
'name': Sort by the function name.
'nfl': Sort by (name, file, line), which is the default.
'pcalls': Sort by the number of primitive calls.
'stdname': Sort by the standard name (this is the name as it appears in the profile).
'time': Sort by internal time spent in the function.
"""

# cProfile.run('App.get_instance().start()')
cProfile.run('App.get_instance().start()', sort='cumtime')
# cProfile.run('App.get_instance().start()', sort=('cumtime', 'calls'))

TODO = """
{} add cacheing to gamelib.text

{} change mask on 'crab' to his mouth, adjust speed (quicker when closer)

{} add a 'game over' screen ( have it fade in, show stats, then kick user to main menu )
- maybe I can take a screenshot of the game over screen and use that as the background for the stats screen(?)

{} fix exit 'pinwheel' bug

{} optimize draw functions... no more blitting, just draw the sprites directly to the screen {} <-- these were suggested from copilot *shrug*
- store the sprites in a list, then draw them all at once (?) {} <-- these were suggested from copilot *shrug*
{{}} what I really want to do is store any rotated imates and only recalculate them when the angle changes

"""