import requests
from bs4 import BeautifulSoup
import re


class Scrapper():

    def __init__(self, query, N):
        baseUrl = 'https://www.google.co.in/search?&q='
        query = query.replace(' ', '+')
        self.url = baseUrl+query
        self.N = N
        
    def getLinks(self):
        urls = []
        cleanUrls = []
        for i in range((self.N-1)/10):
            r=requests.get(self.url+"&start="+str(i*10))
            content = r.content
            soup = BeautifulSoup(content)
            soup = BeautifulSoup(str(soup.find_all("div", {"id": "ires"})))
            links = soup.find_all('a')
            for link in links:
                urls.append(str(link.get("href")))
            for url in urls:
                cleanurl = ' '.join(re.findall(r'https*://\S+&s', url))
                cleanurl = cleanurl[:-2]
                if 'webcache' in cleanurl:
                    continue
                elif cleanurl == '':
                    continue
                else:
                    cleanUrls.append(cleanurl)
        return cleanUrls


