import requests
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import re


def download(url, retries):
    """Download a webpage and returns html code"""

    print("Downloading", url, "...")
    user_agent = {"User-agent": "PythonScraper"}

    try:
        r = requests.get(url, headers=user_agent)
    except:
        if retries > 0:
            print("Waiting to reconnect...")
            sleep(10.0)
            return (download(url, retries-1))
        else:
            raise Exception("Superat maxim nombre d'intents de descarrega")

    return r.text

def parse_works(html):
    """Parse html and get BWV, title and key from Bach's works"""

    df = pd.DataFrame(columns=['bwv','title','key'])
    bs = BeautifulSoup(html, "html.parser")
    for table in bs.find_all('table'):
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            bwv = cols[0].text.strip()
            title = cols[2].text.strip()
            key = cols[3].text.strip()

            x = {'bwv':bwv, 'title':title, 'key':key}
            df = df.append(x, ignore_index=True)

    return df


def clean_works(df):
    """Clean works dataframe"""

    # BWV
    df['bwv'] = df['bwv'].apply(lambda x: re.sub('/1', '', x))

    # Exclude last rows
    df = df.iloc[:-3, :]

    return df


def get_works():
    """Return a list of works of Bach in a dataframe"""

    URL = 'https://imslp.org/wiki/List_of_works_by_Johann_Sebastian_Bach'
    html = download(URL, 3)
    works = parse_works(html)
    works = clean_works(works)

    return works
