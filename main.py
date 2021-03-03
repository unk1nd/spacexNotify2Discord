import requests
import json
import time
import bs4
import os.path
import os
from os import path

apiKey = "FARDIN"
channelId = "UCtI0Hodo5o5dUb67FeUjDeA"
url = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=%s&type=video&eventType=live&key=%s" % (channelId, apiKey)
discordWH = "https://discord.com/api/webhooks/816699292873261067/MORDI"
firstChecker = "https://www.youtube.com/channel/spacexchannel/live"
processedFolder = "processed"
isLive = False
waitTime = 60

# check if process folder exists, if not create it
if not os.path.exists(processedFolder):
    os.mkdir(processedFolder)

while(True):
    # check if live without draining quota from googles api
    x = requests.get(firstChecker)
    html = bs4.BeautifulSoup(x.text, features="html.parser")

    # if "Watching right now" in the html for the page, then scrape data from api endpoint
    if "ser på nå" in html.prettify():
        if not isLive:
            x = requests.get(url)
            data = json.loads(x.content)

            if data["pageInfo"]["totalResults"] > 0:
                print("LIVE")
                for obj in data["items"]:

                    # Collect data
                    videoId = obj["id"]["videoId"]
                    videoURL = "https://www.youtube.com/watch?v=%s" % videoId
                    title = obj["snippet"]["title"]
                    description = obj["snippet"]["description"]
                    content = "SpaceX is now live on youtube with %s" % title
                    thumbnail = obj["snippet"]["thumbnails"]["medium"]["url"]
                    filepath = processedFolder + "/" + videoId

                    # Construct Discord Payload
                    discordData = {
                        "content":content,
                        "embeds": [
                            {
                                "title": title,
                                "type": "rich",
                                "description": description,
                                "url": videoURL,
                                "image": {
                                    "url": thumbnail
                                }
                            }
                        ]
                    }

                    # check if processed before
                    if not path.exists(filepath):
                        # Send Payload to Discord
                        r = requests.post(discordWH, json=discordData)

                        #Store in processed Folder
                        f = open(filepath, "a")
                        f.write("--Processed--")
                        f.close()
                isLive = True
            else:
                print("No New data found in api")
        else:
            print("API could not find any LIVE data for channel")
    else:
        isLive = False
        print("Channel is not live on YT")
    time.sleep(waitTime)
