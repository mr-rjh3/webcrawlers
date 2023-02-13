import argparse
import os.path
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from hashlib import blake2b

def scrapeURL(URL, maxdepth, rewrite, verbose):
    # Fine the hash of the URL
    H = blake2b(bytes(URL, encoding='utf-8')).hexdigest()

    # check if H.txt exists (H is the hash of the URL)
    if(os.path.isfile(H + ".txt") and not args.rewrite):
        # File exists, however we do not want to rewrite it so we will exit
        print("File already exists")
        exit(1)

    # either the file does not exist or we want to rewrite it so we will continue to scraping the URL

    # Get the page / URL to scrape
    print("Spraping URL: ", URL)
    page = requests.get(URL)

    # Create / rewrite the file
    with open(H + ".txt", "w") as f:
        f.write(page.text)

    # Initialize the BeautifulSoup object from the file we just created
    with open(H + ".txt", "r") as f:
        soup = BeautifulSoup(bytes(f.read(), encoding="utf-8"), "html.parser")

    # Extract the links from the page
    links = soup.findAll("a", href=True)

    for link in links:
        print(link["href"])
        
    # Write to the log file
    with open("crawler1.log", "a") as f:
        # <H,URL,Download DateTime, HTTP Response Code>
        f.write("<" + H + ", " + URL + ", " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ", " + str(page.status_code) + ">\n")
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Web scraper for a given URL.')
    parser.add_argument("-url", "--URL", help="Supplies the URL to scrape", required=True)
    parser.add_argument("-d", "--maxdepth", help="Maximum number of depths to crawl from initialURL.", default=10, type=int)
    parser.add_argument("-r", "--rewrite", help="if value is True and file H.txt exists for current URL, it re-download and re-write URL. Otherwise, skips step 2-5. Default value is False.", action="store_true", default=False)
    parser.add_argument("-v", "--verbose", help="if True, print <URL,depth> on the screen. Default value is False.", action="store_true", default=False)
    args = parser.parse_args()
    
    scrapeURL(args.URL, args.maxdepth, args.rewrite, args.verbose)