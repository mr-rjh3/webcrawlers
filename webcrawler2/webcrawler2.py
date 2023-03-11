import argparse
import json
import os.path
import time
import requests
from bs4 import BeautifulSoup
from hashlib import blake2b

def scrapeURL(URL, rewrite, bypass):
    # Find the hash of the URL
    H = blake2b(bytes(URL, encoding='utf-8')).hexdigest()

    # check if H.txt does not exist or we wish to rewrite it (H is the hash of the URL)
    if(not bypass and not os.path.isfile("pages/" + H + ".txt") or rewrite):
        # Scrape the URL and save it to H.txt
        print("Scraping URL: ", URL)
         # try to get the page / URL to scrape
        try:
            # user_agents = [ 
            #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
            #     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
            #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
            #     'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
            #     'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36' 
            # ] 
            # user_agent = random.choice(user_agents) 
            # headers = {'User-Agent': user_agent} 

            s = requests.Session()
            s.auth = ('user', 'pass')
            s.headers.update({'x-test': 'true'})
            time.sleep(1)
            page = s.get(URL)
            if(page.status_code != 200):
                raise Exception("HTTP Response Code: " + str(page.status_code))

        except Exception as e:
            print("Error!!! Could not scrape URL: ", URL, " | Exception: ", e)
            return
        with open("pages/"+ H + ".txt", "w", encoding="utf-8") as f:
            f.write(page.text)

    # Initialize the BeautifulSoup object from our H.txt file
    if(bypass): 
        with open("pages/Google_Scholar.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(bytes(f.read(), encoding="utf-8"), "html.parser")
    else:
        with open("pages/"+ H + ".txt", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(bytes(f.read(), encoding="utf-8"), "html.parser")

    researcher = {}
    researcher["researcher_link"] = URL
    # Extract researcher name and their URLs from the page
    name = soup.find("div", {"id": "gsc_prf_in"}).text
    researcher["researcher_name"] = name
    # print("name:", name)
    # Researcher caption
        # caption = soup.find("div", {"id": "gsc_prf_il"}).text
        # print(caption)
    # Researcher institution
    institution = soup.find("div", {"class": "gsc_prf_il"}).text
    researcher["researcher_institution"] = institution
    # print("institution:", institution)
    # # Researcher keywords
    keywords = []
    for keyword in soup.findAll("a", {"class": "gsc_prf_inta gs_ibl"}):
        keywords.append(keyword.text)
    researcher["researcher_keywords"] = keywords
    # print("keywords:", keywords)
    # Researcher img URL
    img = soup.find("img", {"id": "gsc_prf_pup-img"})["src"]
    researcher["researcher_imgURL"] = img
    # print("img:", img)
    # Researcher stats (citations, h-index, i10-index)
    stats = []
    for stat in soup.findAll("td", {"class": "gsc_rsb_std"}):
        stats.append(stat.text)
    # citations
    citations = {"all": stats[0], "since2018": stats[1]}
    researcher["researcher_citations"] = citations
    # print("citations:", citations)
    # h-index
    h_index = {"all": stats[2], "since2018": stats[3]}
    researcher["researcher_hindex"] = h_index
    # print("h-index:", h_index)
    # i10-index
    i10_index = {"all": stats[4], "since2018": stats[5]}
    researcher["researcher_i10index"] = i10_index
    # print("i10-index:", i10_index)
    # Researcher co-authors
    co_authors = []
    for co_author in soup.findAll("span", {"class": "gsc_rsb_a_desc"}):
        info = {}
        info["coauthor_name"] = co_author.find("a").text
        info["coauthor_title"] = co_author.find("span", {"class": "gsc_rsb_a_ext"}).text
        info["coauthor_link"] = co_author.find("a")["href"]
        co_authors.append(info)
    researcher["researcher_coauthors"] = co_authors
    # print("co-authors:", co_authors)

    # Researcher papers
    papers = []
    for paper in soup.findAll("tr", {"class": "gsc_a_tr"}):
        info = {}
        info["paper_title"] = paper.find("a", {"class": "gsc_a_at"}).text
        info["paper_authors"] = paper.find("div", {"class": "gs_gray"}).text
        info["paper_citedby"] = paper.find("a", {"class": "gsc_a_ac gs_ibl"}).text
        info["paper_year"] = paper.find("span", {"class": "gsc_a_h gsc_a_hc gs_ibl"}).text
        papers.append(info)
    researcher["researcher_papers"] = papers
    # print(papers)

    print("Writing to JSON file...")
    with open("researchers/" + H + ".json", "w", encoding="utf-8") as f:
        json.dump(researcher, f, indent=4)

    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Web scraper for a Google Scholar page.')
    parser.add_argument("URL", type=str, help="The researcher URL to start crawling from")
    parser.add_argument("-r", "--rewrite", help="If True and the file H.txt exists for the current URL re-download and re-write the file. Default value is False.", action="store_true", default=False)
    parser.add_argument("-b", "--bypass", help="Google Scholar has strict webcrawling protections, this program may be prevented to crawl the page due to this. As a way to bypass this you can use this flag to read from a downloaded HTML file instead. Please note that a URL will still be required for hashing purposes. Ensure the file is saved in the 'pages' folder and named 'Google_Scholar.html'. Default value is False", action="store_true", default=False)
    args = parser.parse_args()
    print("Scraping " + args.URL + "...")
    scrapeURL(args.URL, args.rewrite, args.bypass)