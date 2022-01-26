# Tautulli-notranscode-script


## Requirements

Python3 / requests (usually included with python3)<br>
Tautulli (fantastic app that you should be using and must for this script anyway)<br>
PlexPass

This script allows you to stop streams that use trancoding.
Prohibits the use of plex web.
Allow all users to transcode for SD streams

## Edit the bash script (KillstreamLoop.sh):

In this file you need to edit this line: "cd /YOURPATH/killstreamloop.sh && python3 killstream.py" <br>
Specifically you need to edit this part: "/YOURPATH/Tautulli_IP_Enforcer" <br>

## To allow accounts to transcode:

Edit the file "authorized.txt" and add the username id followed by a semicolon and the limit of unique IP addresses that are allowed. <br>For example:<br><br>52252389<br>56428612<br><br>will allow 2 precise accounts to transcode streams for this Plex server. If a user is not in the text file then they can't transcode streams. They have to use direct stream or direct play.

<br><br><br>
Script based on https://github.com/Dosk3n/Tautulli_IP_Enforcer
