# Webcrawlers

## Prerequisites
1. Download and install [python](https://www.python.org/downloads/)
2. Clone the repo
3. Run `pip -r requirements.txt`

## Webcrawler 1
Extracts all links from a given URL and extracts all links from those URLs as well. Continues until MAX DEPTH is reached.

### Usage
1. cd to ./webcrawler1 `cd webcrawler1`
2. Run `python ./webcrawlerX.py URL [-OPTIONS]`

### Options
`URL`
  - The initial URL to start crawling from.

`-d MAXDEPTH`, `--maxdepth MAXDEPTH`
  - Maximum depth the program is allowed to crawl from initialURL. `Default value = 3`

`-r`, `--rewrite`
  - If True while the file H.txt exists for the current URL, re-download and re-write the file. Default value is False.

`-v`, `--verbose`
  - if True, print <URL,depth> to the console for each URL crawled. Default value is False.
  
## Webcrawler 2
Downloads content from a given Google Scholar profile and stores data to a unique JSON file.

### Usage
1. cd to ./webcrawler2 `cd webcrawler2`
2. Run `python ./webcrawler2.py URL [-OPTIONS]`

### Options
`URL`
  - The researcher URL to crawl.

`-r`, `--rewrite`
  - If True while the file H.txt exists for the current URL, re-download and re-write the file. Default value is False.

