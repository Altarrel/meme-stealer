import os
import datetime

import requests

valid_endings = (".jpg", ".png", ".jpeg")

def get_memes(date, limit):
    # Get 50-ish hot memes from r/dankmemes
    payload = {"limit": limit}
    headers = {"User-Agent": "python:meme-stealer:v0.0.2 (by /u/altarrel)"}
    r = requests.get("https://www.reddit.com/r/dankmemes/hot.json", params=payload, headers=headers)
    if r.status_code != requests.codes.ok:
        print("Something went wrong with the request.")
        print(r.status_code)
        print(r.headers)
        r.raise_for_status()
        exit()
    img_urls = []
    for post in r.json()["data"]["children"]:
        
        if "url" not in post["data"]:
            print("Missing url")
            continue
        if any(post["data"]["url"].endswith(x) for x in valid_endings):
            img_urls.append(post["data"]["url"])
            print("Added {} to img_urls".format(post["data"]["url"]))

    # Make sure the directories we will use exist
    if not os.path.exists("./images"):
        os.makedirs("./images")
        os.makedirs("./images/{}".format(date))
    if not os.path.exists("./images/{}".format(date)):
        os.makedirs("./images/{}".format(date))
    else:
        print("Found previous meme folder for today, emptying it.")
        files = os.listdir("./images/{}".format(date))
        for file_name in files:
            os.remove("./images/{}/{}".format(date, file_name))

    i = 0
    for url in img_urls:
        extension = url[url.rfind("."):]
        img = requests.get(url)
        path = "images/{}/{}{}".format(date, str(i), extension)
        with open(path, "wb") as f:
            f.write(img.content)
        print("Downloaded {}".format(url))
        
        i += 1
    
    return "./images/{}".format(date)