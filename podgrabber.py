import re
import urllib.request
import feedparser #hat tip to feedparser -- really useful!
import shutil
import eyed3


# make a dictionary of podcasts and their RSS URLs 
POD_URL_DICT = {
    '#Insert Podcast Name 1' : '#Insert Podcast 1 RSS feed (easy to find via http://getrssfeed.com/)',
    '#Insert Podcast Name 2' : '#Insert Podcast 2 RSS feed (easy to find via http://getrssfeed.com/)',
    '#Insert Podcast Name 3' : '#Insert Podcast 3 RSS feed (easy to find via http://getrssfeed.com/)',
    '#Insert Podcast Name 4' : '#Insert Podcast 4 RSS feed (easy to find via http://getrssfeed.com/)'
    }

def main():
    print()
    print("\n Hey there, I'm Pod Grabber.")
    print()

    while True: #rerun

        current_link_no = 0 #set up the integer to be passed to the feed entry to start at the first feed, then iterate

        key_inputs = [] #set up a list of podcasts to download, one by one

        pod_options = list(POD_URL_DICT.keys())

        print ("Here are your podcast options today: \n")

        for x in pod_options:
            print('==> ' + x)
            
        first_key_input = input("\n Type any one of these names to select the podcast I will help you download:\n\n")

        key_inputs.append(first_key_input) #each podcast is appended to the podcast list

        print("\nGreat! \n\n** If ** you'd like to select another, here the same list again: \n")

        for x in pod_options:
            print('==> ' + x)

        while True: #continue appending until user types "READY"
            next_key_input = input("\nTo add another podcast, just type its name. \n\n\
(I'll ask again, so you can keep entering one name per ask.) \n\nOtherwise, type <READY> in ALL CAPS and I can help you pick (an) episode(s). \n\n")
            if next_key_input != "READY":
                key_inputs.append(next_key_input)
            if next_key_input == "READY":
                break

        print("\nOK, ready!")    

        for dict_key in key_inputs: #each podcast runs through episode by episode until the user wants to download one
            try:
                pod_val = (POD_URL_DICT[dict_key])

                feed = feedparser.parse(pod_val) #pass the podcast rss url to feedparser.parse

                link = feed.entries[current_link_no].enclosures[0].href #see feedparser documentation (https://pythonhosted.org/feedparser/reference-entry-enclosures.html#)
                title = feed.entries[current_link_no].title
                        
                print("\nAlright, so now it's time to select the episode of <" + dict_key + "> you want to download. \n \n\
The most recent episode is entitled <" + title + ">, \n\nand its URL is: <" + link + "> \n") #I print out the URL just in case it contains useful
                                                                                             #info, for example when choosing a filename.

            #Index error may be due to an RSS entry that summarizes the entire show and therefore contains no mp3
            #so move on from the 0th to the 1th entry and rerun
            except IndexError: 
                current_link_no += 1
                link = feed.entries[current_link_no].enclosures[0].href
                title = feed.entries[current_link_no].title
                print("\nAlright, it's time to select the episode of <" + dict_key + "> you want to download. \n \n\
The most recent episode is entitled <" + title + ">, \n\nand its URL is: <" + link + ">.")
                pass
    
            whilename = " "
            while True:
                download_next_or_nix = input("You have three options: \n\n\
1) If you want to download THIS episode, type <DOWNLOAD> in ALL CAPS; \n\n\
2) If instead you want to download the next most recent episode, type <NEXT EPISODE> in ALL CAPS; \n\n\
3) And if you don't want to download this podcast anymore at all, type <NOT THIS POD> in ALL CAPS. \n\n") #Lets user download episode, look at next episode, or move on to next podcast/exit program
                if download_next_or_nix == "NEXT EPISODE":
                    current_link_no += 1
                    print("\nNext! \n\n\
The next most recent episode of <" + dict_key + "> is entitled <" + feed.entries[current_link_no].title + ">, \n \n and its URL is: <" + feed.entries[current_link_no].enclosures[0].href + ">. \n\n\
Same drill . . . \n")
                    continue
                if download_next_or_nix == "DOWNLOAD":
                    pod_folder = "C:\\Users\\INSERTUSERNAMERIGHTHERE\\Music\\iTunes\\iTunes Media\\Automatically Add to iTunes\\" #Replace INSERTUSERNAMERIGHTHERE w/ your Windows User Name
                    file_name = input("\nLast step for this episode: pick a file name to find it in iTunes. \n\n\
(Don't add the filetype <.mp3> to your answer.) \n\n")  
                    file_address = pod_folder + file_name + ".mp3"
                    stage_folder = "C:\\Users\\INSERTUSERNAMERIGHTHERE\\Desktop\\" #Replace INSERTUSERNAMERIGHTHERE w/ your Windows User Name
                    stage_address = stage_folder+"temporaryname.mp3"
                    
                    #Download MP3 podcast with urllib
                    urllib.request.urlretrieve(feed.entries[current_link_no].enclosures[0].href, stage_address) 
                    try:
                        audio = eyed3.load(stage_address)
                        eyed3.log.setLevel("ERROR")
                        audio.tag.artist = u"PODCAST"
                        audio.tag.title = file_name
                        audio.tag.save()
                    except:
                        print ("Insignificant naming error - maybe add details to audiofile directly in iTunes") #Eyed3 sometimes hiccups, which is fine
                        pass

                    shutil.copy2(stage_address, file_address)
                    print("\nEpisode Downloaded.")
                    break
                if download_next_or_nix == "NOT THIS POD":
                    print("\nNo worries!")
                    break

        answer = input("\nAnd we are all set. Type CLOSE in ALL CAPS to exit, or type literally anything else to run again. \n\n")
        if answer == "CLOSE":
                break

if __name__ == "__main__":
    main()

        
