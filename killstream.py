from re import L
from TautulliApiHandler import TautulliApiHandler
import datetime
import time
import argparse
### PUT YOUR VARIABLES ###
def GetTautInfo():
    tautulliIp   = ""                      # IP Address of Tautulli
    tautulliPort = 7181                             # Port of Tautulli
    tautulliApi  = "" # API Key for Tautulli
    # Message to display to a user of a blacklisted IP
    blackListMsg = "-TRANSCODE-"
    concurrentMsg = "PLEX TRANSCODE ENFORCER - YOU ARE NOT ALLOWED TO TRANSCODE STREAMS"
    
    return tautulliIp, tautulliPort, tautulliApi, blackListMsg, concurrentMsg


#function to add userid to purgatory.txt
def AddToPurgatory(userid):
    try:
        f = open("purgatory.txt", "a")
        f.write(str(userid) + "\n")
        f.close()
    except:
        print("There was a problem adding the user to the purgatory list")
        pass
#function to remove userid from purgatory.txt
def RemoveFromPurgatory(userid):
    try:
        f = open("purgatory.txt", "r")
        lines = f.read().splitlines() # Use this rather than readlines so we remove the newline character
        f.close()
        lines = [int(i) for i in lines]

        if userid in lines:
            lines.remove(userid)
            f = open("purgatory.txt", "w")
            for line in lines:
                f.write(str(line) + "\n")
            f.close()
    except:
        pass
#function to check if user is in purgatory.txt
def CheckPurgatory(userid):
    try:
        f = open("purgatory.txt", "r")
        lines = f.read().splitlines() # Use this rather than readlines so we remove the newline character
        f.close()
        lines = [int(i) for i in lines]
        print(lines)
        if userid in lines:
            RemoveFromPurgatory(userid)
            AddToAuthorized(userid)
            return True
        else:
            print("User added to purgatory")
            AddToPurgatory(userid)
            return False
    except:
        pass
#function to add line to authorized.txt
def AddToAuthorized(userid):
    try:
        f = open("authorized.txt", "a")
        
        f.write(str(userid) + "\n")
        f.close()
    except:
        print("There was a problem adding the user to the authorized list")
        pass
def GetConcSettings():
    try:
        f = open("authorized.txt", "r")
        lines = f.read().splitlines() # Use this rather than readlines so we remove the newline character
        f.close()
        lines = [int(i) for i in lines]

        return lines
    except:
        pass

def EnforceConcurrent(tActivitySessions, tapi, concurrentMsg,web,mediaplayer,sd):
    try:
        concSettings = GetConcSettings()

        dataByUser = {}
        # Loop through each session and add to a dictionary where key is the username
        for session in tActivitySessions:
            if(session["user"] in dataByUser):
                # User is already in the dictionary so append to that users array
                dataByUser[session["user"]].append(session)
            else:
                # User isnt in dictionary so add key data pair with username as key and an ampty array as data
                dataByUser[session["user"]] = []
                dataByUser[session["user"]].append(session) # Append that session to the array of that user

        # By this point we have a dictionary of current users with their apropriate sessions
        for cle,valeur in dataByUser.items():



            #print(valeur)
            for j in range(len(valeur)) :

                userid = valeur[j].get('user_id')
                stream_video_resolution = valeur[j].get('stream_video_resolution')



                if userid not in concSettings:

                    print(str(userid) + " : User unauthorized")

                    if(mediaplayer == True or web == True):
                        if(valeur[j].get('product') == 'Plex Media Player' and mediaplayer == True) :
                            concurrentMsg = "PLEX ENFORCER - YOUR MEDIA PLAYER IS DEPRECATED"
                        if(valeur[j].get('product') == 'Plex Web' and web == True) :
                            concurrentMsg = "PLEX ENFORCER - YOUR ARE NOT AUTHORIZED TO USE PLEX WEB"
                        tapi.TerminateSession(valeur[j].get('session_key'), concurrentMsg)
                        print(str(userid) + " : Terminating sessions")
                        EnforcementLogger(valeur[j].get('friendly_name'), "transcode")
                    
                    if(valeur[j].get('video_decision') == 'transcode' and valeur[j].get('state') != 'paused' and (( intro == True) and (valeur[j]["stream_video_full_resolution"] == 'SD' ) ) ):
                        if CheckPurgatory(userid) == True:
                            print(str(userid) + " : User is in purgatory, moved to authorized")
                            concurrentMsg = "NOTICE! - You are playing at a lower quality! You won't see this message again but your access may be revoked in the future if you don't set to Play Original Quality."
                            tapi.TerminateSession(valeur[j].get('session_key'), concurrentMsg)
                            print(str(userid) + " : Terminating sessions")
                            EnforcementLogger(valeur[j].get('friendly_name'), "transcode")
                        else:
                            print(str(userid) + " : User is not in purgatory but not authorized, added to purgatory")
                            concurrentMsg = "NOTICE! - You are playing at a lower quality! set the quality to Play Original! This message will appear again if you don't :("
                            tapi.TerminateSession(valeur[j].get('session_key'), concurrentMsg)
                            print(str(userid) + " : Terminating sessions")
                            EnforcementLogger(valeur[j].get('friendly_name'), "transcode")
                    elif(valeur[j].get('video_decision') == 'transcode' and valeur[j].get('state') != 'paused' and (( sd == True) and (valeur[j].get(stream_video_resolution) != 'sd' ) ) ):
                            concurrentMsg = "NOTICE! - You are playing at a lower quality! set quality to Play Original! This message will appear twice if you don't."
                            tapi.TerminateSession(valeur[j].get('session_key'), concurrentMsg)
                            print(str(userid) + " : Terminating sessions")
                            EnforcementLogger(valeur[j].get('friendly_name'), "transcode")
                            

                else :
                    print(str(userid) + " : User authorized")





    except:
        pass



def EnforcementLogger(message, reason):
    try:
        now = datetime.datetime.now()
        preStringDate = now.strftime("%Y-%m-%d %H:%M:%S")

        if(reason == "transcode") :
            f = open("enforce_log.txt", "a")
            f.write(preStringDate  + " : " + message + "\n")
            f.close()
        else :
            f = open("multiple_streams.txt", "a")
            f.write(reason  + " : " + message + "\n")
            f.close()

    except:
        print("There was a problem logging the error")
        pass

if __name__ == "__main__":
    print("\nStarting Killstream")
    mediaplayer = False
    web = False
    sd = False
    intro = False
    parser = argparse.ArgumentParser(description='monitor plex activity')
    parser.add_argument('-web', '-w', help='Kill streams to unauthorized web clients', action='store_true')
    parser.add_argument('-sd', '-s', help='Allow streams to transcode to sd resolution', action='store_true')
    parser.add_argument('-mediaplayer', '-m', help='Kill streams to unauthorized Plex Media Player', action='store_true')
    parser.add_argument('-intro', '-i', help='Stop new user from transcoding twice and add to authorized', action='store_true')

    args = parser.parse_args()
    if args.web == True:
        web = True
    if args.mediaplayer == True:
        mediaplayer = True
    if args.sd == True:
        sd = True
    if args.intro == True:
        intro = True
    print(intro)
    tIP, tPORT, tAPIKEY, blackListMsg, concurrentMsg = GetTautInfo()
    tapi = TautulliApiHandler(tIP, tPORT, tAPIKEY)
    tActivityData = tapi.GetActivity()
    if(int(tActivityData["stream_count"]) > 0):
        print("There are currently " + str(tActivityData["stream_count"]) + " streams active")

        #EnforceIpBans(tActivityData["sessions"], tapi, blackListMsg) # Check and Enforce IP bans



        EnforceConcurrent(tActivityData["sessions"], tapi, concurrentMsg,web,mediaplayer,sd) # Check and Enforce Concurrent Limits

    else:
        print("No streams found")

        
