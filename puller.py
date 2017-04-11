#!usr/bin/python

import os
import urllib.request
import re
import time
import random

def get_latest_commic():
    temporary = urllib.request.urlopen('https://xkcd.com')
    temporary = str(temporary.read())
    permalink  = re.search("https://xkcd.com/\d+", temporary)
    #uses regular expression to search for the url and any number after
    temporary = permalink.group()
    number = temporary.split('m/')[-1]
    return int(number)

def retrieve_and_save_images(image_url):
    name = image_url[image_url.find("s/") + 2:]
    try:
        image = urllib.request.urlopen(image_url)
    except urllib.error.URLError:
        print("retrival error " + image_url)
        return
    image = image.read()
    path = os.path.join("images", name)
    temporary = open(path, 'wb')
    temporary.write(image)
    print("successfully pulled " + name)

def get_all_urls(number):
    #for i in range(1, number + 1):
    for i in range(407, number + 1):
        url = "https://xkcd.com/%s" % i
        try:
            temporary = urllib.request.urlopen(url)
        except urllib.error.HTTPError:
            print("HTTP Error " + url)
            continue
        temporary = str(temporary.read())
        link_start = temporary.find("https://imgs.xkcd.com/comics/")
        if link_start == -1:
            print("search error " + str(i))
            continue
        else:
            temporary = temporary[link_start:]
        link_end = temporary.find("\\n")
        if link_end == -1:
            print("seach error " + str(i))
            continue
        else:
            temporary = temporary[:link_end]
            image_url = temporary.strip()
            retrieve_and_save_images(image_url)
            if i%50 == 0:
                print("pulled " + str(i) + "/" + str(number))
            time.sleep(random.random())
            
def main():
    number = get_latest_commic()
    get_all_urls(number)
    
main()
