# NS Watch   - I wanted my Rasberry to check if I can drink another coffee at home.. 
#              in case of train trouble. The NS App does the same but not (yet?) for cancelled trains
#              Works with NS API and Telegram. Register at https://apiportal.ns.nl/ to get an NS API token
# Version 1.0- Initial version
#              API URL  used in this code https://gateway.apiportal.ns.nl/public-reisinformatie/api/v2/departures
#              The product API name in the NS store is called RetrieveTripInformationPublicAPI (Dutch and English are mixed)
#              Also included code to work with Telegram. A good tutorial for registering a Bot and getting your chatID is here:
#              https://www.domoticz.com/wiki/Telegram_Bot (kudos to those working on Domoticz who documented that part)
#              One could use the official Telegram API but this version does not need any 'pip install' stuff.
#              Format : https://api.telegram.org/bot123456789:FAKEFAKEFAKEFAKE000FAKEFAKEFAKEFAKE/sendMessage?chat_id=987654321&text=Hello
#                                                   <<                                         >>/sendmessage?chat_id=<<     >>&text=<< >>
#*** END Comment block *****
import requests, json
from datetime import tzinfo, timedelta, datetime
#***************************
#**** YOUR DATA BLOCK ******
#***************************
NSAPITOKEN      = "998877665544FAKEFAKE556677889900"                #replace with your own data
TELEGRAMKEY     = "123456789:FAKEFAKEFAKEFAKE000FAKEFAKEFAKEFAKE"   #replace with your own data
TELEGRAMCHATID  = "987654321"                                       #replace with your own data
STATION2WATCH   = "8400058"    #Amsterdam Centraal=8400058, Utrecht CS= 8400621 .. and so on.. 
                               #Research your station UICCode via API getAllStations, NS made a nice web GUI and interface to try APIs
TIME2WATCH      = "17:24"      # Which departure time do you want to track
DIRECTION2WATCH = "Nijmegen"   # Which departing direction do you want to track
#***************************
#***************************

# Function to send a Telegram message via the ugly way - no use of standard Telegram API library
def SendTelegram(obj):
    url = "https://api.telegram.org/bot"+TELEGRAMKEY+"/sendMessage"
    payload = {
        'chat_id': TELEGRAMCHATID,  #see your data block
        'text': obj                 #<<--- message text goes here and is set at calling the function SendTelegram >>
    }
    response = requests.post(url, payload)
    #data = response.json()   #for debug purposes
    #print(data)              #for debug purposes


#START of NS API call - starting with definitons and tokens
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': NSAPITOKEN,  #<<--- NS API Public-Travel-Information subscription token - see your data block
}
payload = {
    'maxJourneys': '25',  #Does not seem to work
    'lang': 'nl',         #Does not really make a difference
    'uicCode': STATION2WATCH  #<<---Station code for your NSWatch software
}
url = "https://gateway.apiportal.ns.nl/public-reisinformatie/api/v2/departures"
response = requests.get(url, payload, headers=headers)
data = response.json()
#determine number of returned departures in the payload section of the JSON that was returned from the NS API
itemsinjson = len(data['payload']['departures'])
#print(itemsinjson) #for test purposes

#Process the whole list.. actually it will not loop the last time so -1 is not needed
for x in range(0, (itemsinjson)): 
    row=str(x)
    whereto = str(data['payload']['departures'][x]['direction'])
    planning = str(data['payload']['departures'][x]['plannedDateTime'])
    niceplanning =str(planning[11:16])  #Get rid of date part
    datetime_planning = datetime.strptime(planning[0:19], '%Y-%m-%dT%H:%M:%S')
    # See https://www.journaldev.com/23365/python-string-to-datetime-strptime ..beware that %z does not work on Python 2.7 Hence the partial use 0:19
    actual = str(data['payload']['departures'][x]['actualDateTime'])
    datetime_actual = datetime.strptime(actual[0:19], '%Y-%m-%dT%H:%M:%S')
    wherestatus = str(data['payload']['departures'][x]['departureStatus'])
    whereisit = str.lower(wherestatus)           #removing the capitals
    iscancelled = str(data['payload']['departures'][x]['cancelled'])
    timedelta=datetime_actual-datetime_planning  #Now we can work with the variables and calculate delay time
    delay=str(timedelta)                         #The string representation is needed as well
    #The print part looks nice but does not have a use when it is fired by CRON.. but still it is handy for debugging
    print(row+" Train to "+whereto+" from "+niceplanning+" is "+whereisit+" Delay="+delay+" Cancelled="+iscancelled) 
    #Is there a message needed for this row? Lets do some checking..
    #Is a train delayed on the time and direction we are watching?
    if (whereto == DIRECTION2WATCH) and (niceplanning==TIME2WATCH) and (delay != "0:00:00" ):
         print("Send Telegram - Specific delayed train") #Debugging only
         message = "Train to "+DIRECTION2WATCH+" from "+TIME2WATCH+" is delayed by "+delay
         SendTelegram(message)
    #Is a train cancelled on the time and direction we are watching?
    elif (whereto == DIRECTION2WATCH) and (niceplanning==TIME2WATCH) and (iscancelled == "True"):
         print("Send Telegram - Train cancelled - drink coffee where you are") #Debugging only
         message = "!! Train to "+DIRECTION2WATCH+" from "+TIME2WATCH+" is Cancelled"
         SendTelegram(message)
    #Is there any delay in the station we are watching? Nice for debugging loop
    #elif (delay != "0:00:00" ):
    #     print("Send Telegram - Delayed train") #Debugging only
    #     message = "Train to "+whereto+" from "+niceplanning+" is delayed by "+delay+" and "+whereisit
    #     SendTelegram(message)


