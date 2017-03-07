# BejewledBot
A bot to play the steam version of bejeweled 3 in lightning mode, with a focus on speed.

Author: Dillon Thyer

## Notes about running the bot:
1. The autopy library requires adequate administrator/file privellages in order to be allowed to take control and enter mouse input.

2. The stopping clause on the bot is not very good at the moment, so have a plan to close it and only start it when bejewled 3 is open and you are ready. It will attempt to click and drag things around your desktop if your desktop looks enough (pixel color-wise) like a bejewled board, and you do not want it to try and play your desktop, while fighting automatic mouse input to try to close it.


## How to run the bot:
1. ensure you have the following python libraries installed as they are dependancies:
 - PIL (Python imaging library)
 - Autopy library
You can find these easily enough online.

2. Once you have given the script file permissions/are ready to run it as an admin, make sure you have bejewled open and ready first. Then start the script, move anything in the way of the bejewled window away and click on the bejewled window. In 5 seconds of starting the bot will auto resize the window and move it to the top left hand of the corner of your script. The bot will run indefinitely now till you manually close it.

3. navigate your way into the bejewled window, and start a game of bejewled (lightning mode works best). The bot will start playing when the game starts, and next time you play again till you close it it will keep playing.

4. Closing the bot: to have a single convinient keyboard shortcut ready to kill the script is still a tusu, but you can make sure you have something ready to close it. At the end of a game, it should recognise the menu and the mouse will stop moving around. Now  carefully close the bot, making sure not to bring any windows over the bejewled window lest it play your desktop, kill the script.

### If you must exit mid game (not advised):
Press escape and bring up the bejewled menu mid game, hopefully the bot should recognise the menu and stop, then being carefull again,
follow step 4.

### Improvements:
- Easier method to kill the script, e.g. break on a keypress.
- Flashy animations limit accuracy of color recognition, could change/improve the color recognition method.
