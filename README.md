# NSwatch - prelude
This python code uses the NS API to look for changes in your daily train routine. Especially the cancelled trains which are not (yet?) picked up by the regular NS App. The python code will run, scheduled by crontab, monitor your regular trains and send you a Telegram message before you commute to a train station to find your train has been cancelled or delayed. It will run on anything that tolerates python.

# Why?
I like train travels for my daily commute. I do not like the surprise when I walk into the station and see a lot of people waiting due to a cancelled train. Although the NS App has a good alerting function, I could not help noticing that it is lacking the ability to notify in case of cancelled trains. I hear you thinking.. where do all the people go when a train is cancelled? To the same coffee shop.. I rather work from home or desk when this happens and decided to write a bit of code that queries the official NS API.

# How?
Since the Raspberry Pi it has been really easy to run code 24/7 for a few euro's a year. If you own one and are a regular train passenger, this might be for you as well. The code is not really elaborate so if you travel from A --> B and from B --> A daily, I reccommend you copy the script for each route. Be mindfull that the NS changed the API to use tokens instead of a USERID & Password. That is why a lot of NS code snippets are not usable anymore.

# Using it
I have a fairly standardised scheduled daily routine and planned the script to run twice before I walk out the door.. actually, the same script runs twice. One run at 6:45 AM and one at 07:05 AM.. that should flag trouble in time for my particular situation. Only running those at weekdays is easy when you Google a bit on crontab formats. For the journey from B --> A in the afternoon I also scheduled crontab. because of the change of direction I use a copy of the script for this particular direction. One could build it into one.. but let's not over complicate stuff.

# Example of the Crontab:
>#m h  dom mon dow   command
>45 06 * *     1-5 python /home/pi/nswatch/nswatch_v1.0_Amsterdam.py >/dev/null 2>&1
>05 07 * *     1-5 python /home/pi/nswatch/nswatch_v1.0_Amsterdam.py >/dev/null 2>&1
>50 17 * *     1-5 python /home/pi/nswatch/nswatch_v1.0_Utrecht.py >/dev/null 2>&1
>05 18 * *     1-5 python /home/pi/nswatch/nswatch_v1.0_Utrecht.py >/dev/null 2>&1

# Kudos
To the people at NS who opened up this nice API and Web GUI.:+1:
It really inspired me to query the API and learn about JSON, Python and the whole !#
To the people at Telegram :+1: who made it possible to use their messaging platform
To the community working on/ with Domoticz :+1: who documented the creation of credentials & Bot on Telegram

# Links
NS API Documentation: https://apiportal.ns.nl/
The product API name in the NS store is called RetrieveTripInformationPublicAPI
How to get a Telegram communication going: https://www.domoticz.com/wiki/Telegram_Bot
