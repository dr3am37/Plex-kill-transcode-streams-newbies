# Tautulli-transcode-script


## Requirements

Python3 / requests (usually included with python3)<br>
Tautulli (fantastic app that you should be using anyway)<br>
PlexPass

This script allows you to stop streams that use trancoding.
Prohibits the use of plex web.
Add account IDs to authorized.txt file

## Edit the bash script (KillstreamLoop.sh):

In this file you need to edit this line: "cd /home/dean/Tautulli_IP_Enforcer && python3 tautulliIpEnforcer.py" <br>
Specifically you need to edit this part: "/home/dean/Tautulli_IP_Enforcer" <br>
Change this to the path of where you cloned this repository. It must be the path, not just the folder name.

## To allow accounts to transcode:

Edit the file "authorized.txt" and add the username id followed by a semicolon and the limit of unique IP addresses that are allowed. <br>For example:<br><br>52252389<br>56428612<br><br>will allow 2 precise accounts to transcode streams for this server IP addresses for this user. If a user is not in the text file then they can't transcode streams. They have to use direct stream or direct play.

<br><br><br>
Script based on https://github.com/Dosk3n/Tautulli_IP_Enforcer
