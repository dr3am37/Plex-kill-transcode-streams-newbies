from TautulliApiHandler import TautulliApiHandler
import datetime
import time

### PUT YOUR VARIABLES ###
def GetTautInfo():
    tautulliIp   = "x.x.x.x"                      # IP Address of Tautulli
    tautulliPort = 8181                               # Port of Tautulli
    tautulliApi  = "" # API Key for Tautulli
    # Message to display to a user of a blacklisted IP
    blackListMsg = "-TRANSCODE-"
    concurrentMsg = "PLEX TRANSCODE ENFORCER - YOU ARE NOT ALLOWED TO TRANSCODE STREAMS"

    return tautulliIp, tautulliPort, tautulliApi, blackListMsg, concurrentMsg



def GetConcSettings():
    try:
        f = open("authorized.txt", "r")
        lines = f.read().splitlines() # Use this rather than readlines so we remove the newline character
        f.close()
        lines = [int(i) for i in lines]

        return lines
    except:
        pass

def EnforceConcurrent(tActivitySessions, tapi, concurrentMsg):
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
            
            for j in range(len(valeur)) :

                userid = valeur[j].get('user_id')
                stream_video_resolution = valeur[j].get('stream_video_resolution')

                if userid not in concSettings:

                    if(valeur[j].get('product') == 'Plex Web'):
                        tapi.TerminateSession(valeur[j].get('session_key'), concurrentMsg)
                        print("Terminating sessions")

                    elif(valeur[j].get('transcode_decision') == 'transcode' and valeur[j].get('state') != 'paused' and  (stream_video_resolution != 'sd' ) ):
                        tapi.TerminateSession(valeur[j].get('session_key'), concurrentMsg)
                        print("Terminating sessions")
                        
    except:
        pass
    


def EnforcementLogger(message):
    try:
        now = datetime.datetime.now()
        preStringDate = now.strftime("%Y-%m-%d %H:%M:%S")
        f = open("enforce_log.txt", "a")
        f.write(preStringDate + ": " + message + "\n")
        f.close()

    except:
        print("There was a problem logging the error")
        pass

def Main():
    print("\nStarting Killstream")
    tIP, tPORT, tAPIKEY, blackListMsg, concurrentMsg = GetTautInfo()
    tapi = TautulliApiHandler(tIP, tPORT, tAPIKEY)
    tActivityData = tapi.GetActivity()
    if(int(tActivityData["stream_count"]) > 0):
        print("There are currently " + str(tActivityData["stream_count"]) + " streams active")



        EnforceConcurrent(tActivityData["sessions"], tapi, concurrentMsg) # Check and Enforce Concurrent Limits

    else:
        print("No streams found")
    

        

Main()