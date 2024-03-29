# Plex kill transcode streams for new users

This script is based on plex-kill-transcode-streams script but it's aimed at new users not knowing about the "Play origianl quality"
If a 720p 2mpbs stream is detected the stream will be stopped by the script with a message explaining the issue.
the user will be stored in "purgatory" meaning he will get warned again if he does it again but after that will be moved to an authorized list to account for people that could perhaps only play 720p 2mpbs for various reasons.

### Requirements

Python3 / requests (usually included with python3)<br>
Tautulli (fantastic app that you should be using and must for this script anyway)<br>
PlexPass


## Method 1 : run a shell script in background

The script checks every 20 seconds streams activities.

### Install requirements :

run

   ```shell
   user:~/plex-kill-transcode-streams$ sudo pip install -r requirements.txt
   ```

### Edit the bash script (KillstreamLoop.sh):

In this file you need to edit this line: "cd /YOURPATH/killstreamloop.sh && python3 killstream.py" <br>
Specifically you need to edit this part: "/YOURPATH/Tautulli_IP_Enforcer" <br>

### To allow accounts to transcode:

Edit the file "authorized.txt" and add the username id followed by a semicolon and the limit of unique IP addresses that are allowed. <br>For example:<br><br>52252389<br>56428612<br><br>will allow 2 precise accounts to transcode streams for this Plex server. If a user is not in the text file then they can't transcode streams. They have to use direct stream or direct play.


## Method 2 : tautulli runs itself the script  :

Tautulli run the script when a stream starts, resumes or when a stream changes its transcoding decision.

### Install requirements

   ```shell
   user:~/plex-kill-transcode-streams$ sudo pip install -r requirements.txt
   ```

### Edit your tautulli settings

Add a new notifications agent called killstream and edit the configuration and triggers like the following images:
You can add the following script arguments :

-w : Kill all unauthorized streams which use Plex Web as client
-m : Kills all unauthorized streams which use Plex Media Player as client
-s : Allow streams to transcode to sd resolution


<p align="center">
  <img src="./img/settings.png" width="350" title="settings">
</p>

<p align="center">
  <img src="./img/triggers.png" width="350" title="triggers">
</p>
<p align="center">
  <img src="./img/arguments.png" width="350" title="arguments">
</p>

<br><br><br>
Script based on https://github.com/Dosk3n/Tautulli_IP_Enforcer
