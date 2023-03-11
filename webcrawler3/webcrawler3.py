import argparse
import os.path
import re
import time
import requests
from hashlib import blake2b
import plotly.graph_objects as go
from alive_progress import alive_bar

def contentRatio(i, j, text):
    # Finds the number of tags to the left of i + number of words between i and j + number of tags to the right of j
    x = 0
    # find number of tags to left of i
    for k in range(0, i):
        if(text[k] == '1'):
            x += 1
    # find number of words between i and j
    for k in range(i, j):
        if(text[k] == '0'):
            x += 1
    # find number of tags to the right of j
    for k in range(j, len(text)):
        if(text[k] == '1'):
            x += 1
    return x

def plotContentRatio(text):
    # Plot the content ratio of the text using plotly
    x = []
    y = []
    z = []
    with alive_bar(len(text)) as bar:
        for i in range(0, len(text)):
            for j in range(i, len(text)):
                x.append(i)
                y.append(j)
                z.append(contentRatio(i, j, text))
            bar()
    # plot the content ratio using 3d scatter plot from plotly
    print("Plotting content ratio using 3d scatter plot from plotly")
    data = [go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=1, color=z, colorscale='Viridis', opacity=0.8))]
    fig = go.Figure(data=data)
    fig.update_layout(title="Content Ratio", scene = dict(
        xaxis_title='i',
        yaxis_title='j',
        zaxis_title='f(i,j)'))
    fig.show()

    # plot the content ratio using 2d heatmap from plotly
    print("Plotting content ratio using 2d heatmap from plotly")
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=x,
        y=y,
        colorscale='Viridis'))
    fig.update_layout(title="", xaxis_title='i', yaxis_title='j')
    fig.show()

def scrapeURL(URL, rewrite, plot):
    # Find the hash of the URL
    H = blake2b(bytes(URL, encoding='utf-8')).hexdigest()

    # check if H.txt does not exist or we wish to rewrite it (H is the hash of the URL)
    if(not os.path.isfile("pages/" + H + ".txt") or rewrite):
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
            
      # remove all new lines and tabs from the HTML
    with open("pages/"+ H + ".txt", "r", encoding="utf-8") as f:
        # remove all instances of new lines 
        text = f.read().replace('\n', '')
        # remove all instances of tabs
        text = text.replace('\t', '')

        tag_regex = re.compile("<.*?>") # regex to find all HTML tags (assumes HTML tag is in format <????>)
    
        # replace all instances of html tags with the string "1"
        text = re.sub(tag_regex, "1", text)

        # regex that finds all instances of a word (string separated by space characters) not including "1"
        word_regex = re.compile("[^ ,1]+")
        # replace all words with the string "0"
        text = re.sub(word_regex, "0", text)
        # remove all characters that are not 0 or 1
        text = re.sub("[^01]", "", text)

    # write to new file
    with open("pages/NUMBERS-"+ H + ".txt", "w", encoding="utf-8") as f:
        f.write(text)
    
    # plot the content ratio of the text
    if(plot): plotContentRatio(text)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Web scraper for a Google Scholar page.')
    parser.add_argument("URL", type=str, help="The researcher URL to start crawling from")
    parser.add_argument("-r", "--rewrite", help="If True and the file H.txt exists for the current URL re-download and re-write the file. Default value is False.", action="store_true", default=False)
    parser.add_argument("-p", "--plot", help="If True the program will open an interactive 3d Scatter plot and 2d Heatmap in your default browser. Default value is False.", action="store_true", default=False)
    args = parser.parse_args()
    print("Scraping " + args.URL + "...")
    scrapeURL(args.URL, args.rewrite, args.plot)