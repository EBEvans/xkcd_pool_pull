#!/usr/bin/python3

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

def retrieve_and_save_images(image_url, failed_commics):
    name = image_url[image_url.find("s/") + 2:]
    try:
        image = urllib.request.urlopen(image_url)
    except urllib.error.URLError:
        error = "URL error " + image_url + " OR commic number " + str(i)
        print(error)
        failed_commics.append(error)
        return
    image = image.read()
    path = os.path.join("images", name)
    temporary = open(path, 'wb')
    temporary.write(image)
    print("successfully pulled " + name)

def get_all_urls(number, failed_commics):
    for i in range(1, number + 1):
    #for i in range(1, 450):
        url = "https://xkcd.com/%s" % i
        try:
            temporary = urllib.request.urlopen(url)
        except urllib.error.HTTPError:
            error = "HTTP Error " + url + " OR commic number " + str(i)
            print(error)
            failed_commics.append(error)
            continue
        temporary = str(temporary.read())
        link_start = temporary.find("https://imgs.xkcd.com/comics/")
        if link_start == -1:
            error = "image link search error " + str(i)
            print(error)
            failed_commics.append(error)
            continue
        else:
            temporary = temporary[link_start:]
        link_end = temporary.find("\\n")
        if link_end == -1:
            error = "image link search error " + str(i)
            print(error)
            failed_commics.append(error)
            continue
        else:
            temporary = temporary[:link_end]
            image_url = temporary.strip()
            retrieve_and_save_images(image_url, failed_commics)
            if i%50 == 0:
                print("pulled " + str(i) + "/" + str(number))
            time.sleep(random.random())
            
def main():
    try:
        os.mkdir('images')
        print('created images folder/directory')
    except FileExistsError:
        print('images folder/directory already exists; no new directory made')
    failed_commics = []
    number = get_latest_commic()
    get_all_urls(number, failed_commics)
    print("pull complete.")
    print("failed comics:")
    for i in failed_commics:
        print(i)
    
main()
