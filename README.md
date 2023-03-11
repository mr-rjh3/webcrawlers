# Webcrawlers

## Prerequisites
1. Download and install [python](https://www.python.org/downloads/)
2. Clone the repo

## Webcrawler 1
Extracts all links from a given URL and extracts all links from those URLs as well. Continues until MAX DEPTH is reached.

### Usage
1. cd to ./webcrawler1 `cd webcrawler1`
2. Run `pip -r requirements.txt`
3. Run `python ./webcrawlerX.py URL [-OPTIONS]`

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
2. Run `pip -r requirements.txt`
3. Run `python ./webcrawler2.py URL [-OPTIONS]`

### Options
`URL`
  - The researcher URL to crawl.

`-r`, `--rewrite`
  - If True while the file H.txt exists for the current URL, re-download and re-write the file. Default value is False.
  
`-b`, `--bypass`
  - Google Scholar has strict webcrawling protections, this program may be prevented to crawl the page due to this. As a way to bypass this you can use this flag to read from a downloaded HTML file instead. Please note that a URL will still be required for hashing purposes. Ensure the file is saved in the 'pages' folder and named 'Google_Scholar.html'. Default value is False.

## Webcrawler 3
Downloads content from a given URL and uses a function to find the approximate location of the start and end of the content within an HTML page.

### Usage
1. cd to ./webcrawler3 `cd webcrawler3`
2. Run `pip -r requirements.txt`
3. Run `python ./webcrawler3.py URL [-OPTIONS]`

### Options
`URL`
  - The URL to crawl.

`-r`, `--rewrite`
  - If True while the file H.txt exists for the current URL, re-download and re-write the file. Default value is False.
  
`-p`, `--plot`    
  - If True the program will open an interactive 3d Scatter plot and 2d Heatmap in your default browser. Default value is False.
