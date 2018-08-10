import re
import urllib.request
import feedparser
import shutil
import eyed3

podNUrlDict = {'#Insert Podcast Name 1' : '#Insert Podcast 1 RSS feed (easy to find via http://getrssfeed.com/)',
               '#Insert Podcast Name 2' : '#Insert Podcast 2 RSS feed (easy to find via http://getrssfeed.com/)',
               '#Insert Podcast Name 3' : '#Insert Podcast 3 RSS feed (easy to find via http://getrssfeed.com/)',
               '#Insert Podcast Name 4' : '#Insert Podcast 4 RSS feed (easy to find via http://getrssfeed.com/)'} #create a dictionary of podcasts and their rss urls 
print("\n Hey there, I'm Pod Grabber.")
while True: #rerun 
    keyinputs = [] #set up a list of podcasts to download, one by one
    firstkeyinput = input("\n Type any one of these names to select the podcast I will help you download:\n\
                   \n =>   #Insert Pod Name 1 =>    #Insert Pod Name 2\
                 \n\n =>   #Insert Pod Name 3 =>    #Insert Pod Name 4\ \n\n")
    keyinputs.append(firstkeyinput) #each podcast is appended to the podcast list
    while True: #continue appending until user types "READY"
        nextkeyinput = input("\nGreat!\n\n** If ** you'd like to select another podcast as well, type in the next podcast's name. \n\n\
(I'll ask again, so you can keep entering one name per ask.) \n\nOtherwise, type <READY> in ALL CAPS and I can help you pick (an) episode(s). \n\n")
        if nextkeyinput != "READY":
            keyinputs.append(nextkeyinput)
        if nextkeyinput == "READY":
            break
    print("\nOK, ready!")    
    for dictkey in keyinputs: #each podcast runs through episode by episode until the user wants to download one
        try:
            podval = (podNUrlDict[dictkey])

            feed = feedparser.parse(podval) #pass the podcast rss url to feedparser.parse

            currentlinkno = 0 #set up the integer to be passed to the feed entry to start at the first feed, then iterate

            l = feed.entries[currentlinkno].enclosures[0].href #see feedparser documentation (https://pythonhosted.org/feedparser/reference-entry-enclosures.html#)
            t = feed.entries[currentlinkno].title
                        
            print("\nAlright, so now it's time to select the episode of <" + dictkey + "> you want to download. \n \n\
The most recent episode is entitled <" + t + ">, \n\nand its URL is: <" + l + "> \n") #I print out the URL just in case it contains useful
                                                                                      #info, for example when choosing a filename.

        except IndexError: #Index error may be due to an rss entry that summarizes the entire show and therefore contains no mp3, so move on from the 0th to the 1th entry and rerun
            currentlinkno = currentlinkno + 1
            l = feed.entries[currentlinkno].enclosures[0].href
            t = feed.entries[currentlinkno].title
            print("\nAlright, it's time to select the episode of <" + dictkey + "> you want to download. \n \n\
The most recent episode is entitled <" + t + ">, \n\nand its URL is: <" + l + ">.")
            pass
    
        whilename = " "
        while True:
            dlnextornix = input("You have three options: \n\n\
1) If you want to download THIS episode, type <DOWNLOAD> in ALL CAPS; \n\n\
2) If instead you want to download the next most recent episode, type <NEXT EPISODE> in ALL CAPS; \n\n\
3) And if you don't want to download this podcast anymore at all, type <NOT THIS POD> in ALL CAPS. \n\n") #Lets user download episode, look at next episode, or move on to next podcast/exit program
            if dlnextornix == "NEXT EPISODE":
                currentlinkno = currentlinkno + 1
                print("\nNext! \n\n\
The next most recent episode of <" + dictkey + "> is entitled <" + feed.entries[currentlinkno].title + ">, \n \n and its URL is: <" + feed.entries[currentlinkno].enclosures[0].href + ">. \n\n\
Same drill . . . \n")
                continue
            if dlnextornix == "DOWNLOAD":
                podfolder = "C:\\Users\\#Insert Windows User Name\\Music\\iTunes\\iTunes Media\\Automatically Add to iTunes\\"
                filename = input("\nLast step for this episode: pick a file name to find it in iTunes. \n\n\
(Don't add the filetype <.mp3> to your answer.) \n\n")  
                fileaddress = podfolder + filename + ".mp3"
                stagefolder = "C:\\Users\\#Insert Windows User Name\\Desktop\\"
                stageaddress = stagefolder+"temporaryname.mp3"

                urllib.request.urlretrieve(feed.entries[currentlinkno].enclosures[0].href, stageaddress) #Download MP3 podcast with urllib
                try:
                    audio = eyed3.load(stageaddress)
                    eyed3.log.setLevel("ERROR")
                    audio.tag.artist = u"PODCAST"
                    audio.tag.title = filename
                    audio.tag.save()
                except:
                    print ("Insignificant naming error - maybe add details to audiofile directly in iTunes") #Eyed3 sometimes hiccups, which is fine
                    pass
                shutil.copy2(stageaddress, fileaddress)
                print("\nEpisode Downloaded.")
                break
            if dlnextornix == "NOT THIS POD":
                print("\nNo worries!")
                break
    answer = input("\nAnd we are all set. Type CLOSE in ALL CAPS to exit, or type literally anything else to run again. \n\n")
    if answer == "CLOSE":
            break
        
