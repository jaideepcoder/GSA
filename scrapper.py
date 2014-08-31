import requests
from bs4 import BeautifulSoup
import re, urllib


class Scrapper():

    def __init__(self, query, N):
        baseUrlLink = 'https://www.google.co.in/search?&q='
        query = query.replace(' ', '+')
        self.urlLink = baseUrlLink+query

        self.baseUrlFeature = 'http://www.alexa.com/siteinfo/'
        self.N = N
        
    def getLinks(self):
        urls = []
        cleanUrls = []
        for i in range((self.N-1)/10):
            r=requests.get(self.urlLink+"&start="+str(i*10))
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

    def getFeatures(self, url):
        url = urllib.quote_plus(url)
        r = requests.get(self.baseUrlFeature+url)
        content = r.content

        soup = BeautifulSoup(content)
        html = soup.find_all('strong', {'class':'metrics-data align-vmiddle'})
        features = list()
        for data in html:
            text = data.text
            if '%' in text:
                text = float(text[:-1])
            elif '.' in text:
                text = float(text)
            elif ':' in text:
                time = text.split(':')
                for i in range(len(time)): time[i] = int(time[i])
                if len(time) == 3: text = time[0]*3600 + time[1]*60 + time[2]
                elif len(time) == 2: text = time[0]*60 + time[1]
                elif len(time) == 1: text = time[0]
            elif '-' in text:
                text = 0
            else: text = int(text.replace(',', ''))
            features.append(text)
        html = soup.find_all('span', {'class':'font-4'})[0]
        features.append(int(str(html.text).replace(',', '')))
        return features
    
