# *- coding: utf-8 -*
##Threadscan - Info gatherer by [Redacted]##
##Done in 07-07-2023 instead of doing the dishes.
import os
import sys
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests

##Get Threads from user (originated by them and repost with text added by them)
def getthreads(soup):
    fthreads = soup.find_all("div", {'data-pressable-container': 'true'})##Get all individual Thread containers
    for ft in fthreads: #Loop through threads (holy shit that was hard to spell)
        if ft.find("div", {'class' : 'xzueoph'}) == None: #Check if Thread is not a simple repost
            if ft.find("p", {'class' : 'xat24cr xdj266r'}) != None: #Dicard Thread with no text
                print(ft.find("time")['datetime'])##Get thread date value
                print(ft.find("p", {'class' : 'xat24cr xdj266r'}).find("span").text)##Get thread text
                print("=" * 5)
            else: ##Thread with no text (media only) discarded
                pass
        else: ##Simple repost discarded
            pass

##Get media
def getmedia(soup, username): #Threads with Media (pictures and videos) have a div with class=x1xmf6yo
    os.mkdir(username)
    media = 0
    fthreads = soup.find_all("div", {'data-pressable-container': 'true'})
    for ft in fthreads:
        if ft.find("div", {'class' : 'xzueoph'}) == None: #Check if Thread is not a simple repost
            if ft.find("div", {'class' : 'x1xmf6yo'}) != None: #Check if Thread has media div class
                if ft.find_all("img", {'draggable' : 'false'}) != None: #Confirm pictures present
                    for link in ft.find_all("img", {'draggable' : 'false'}):
                        picurl = (link['src']) #Get src url for each picture
                        response = requests.get(picurl)
                        with open('./{}/{}.jpg'.format(username,str(media)), 'wb') as w: 
                            w.write(response.content)
                            media += 1
                else: ##Media but no pics; video then. But havent figured out how to handle this yet, so fuck it
                    pass
            else: ##Thread with no media discarded
                pass
        else: ##Simple repost discarded
            pass

##Get bio, follower number and profilepic link
def getinfo(soup, username):
    print("Bio:")
    print(soup.find("div", {'class' : 'xw7yly9'}).find("span").text) #Get profile bio
    print("="*5)
    print(soup.find("span", {'class' : 'x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xjohtrz xo1l8bm x12rw4y6'}).text)
    ppurl = soup.find("img", {'class' : 'xl1xv1r x14yjl9h xudhj91 x18nykt9 xww2gxu'})['src'] #Profile picture link
    session = HTMLSession()
    response = session.get(ppurl)
    with open('./{}.jpg'.format(username), 'wb') as w: 
        w.write(response.content)

def getuser(username): ##Loads javascript generated content from profile page
    session = HTMLSession()
    url = "https://www.threads.net/@{}".format(username)
    r = session.get(url)
    r.html.render(sleep=4, keep_page=True)
    soup = BeautifulSoup(r.html.raw_html, features='lxml')
    return soup #Returns the complete generated content to pass to the other functions

def usage(): ##Show help
    print("Threadscan V0.1 by Replica")
    print("-h Shows this help message")
    print("-b Gets basic user information; description, number of followers and downloads profile picture")
    print("-t Gets Threads by user (no direct reposts)")
    print("-m Downloads pictures in user's Threads (no direct reposts")
    print("Usage example: threads.py -t username")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        sys.exit()
    else:
        if sys.argv[1] == "-h":
            usage()
        if sys.argv[1] == "-b":
            soup = getuser(sys.argv[2])
            getinfo(soup, sys.argv[2])
        if sys.argv[1] == "-t":
            soup = getuser(sys.argv[2])
            getthreads(soup)
        if sys.argv[1] == "-m":
            soup = getuser(sys.argv[2])
            getmedia(soup, sys.argv[2])
        else:
            print("Idk about that")
