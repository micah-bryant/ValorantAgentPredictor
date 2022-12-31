import requests
from bs4 import BeautifulSoup
import pandas as pd

class BlitzScraper:
    def __init__(self, importParams):
        # TODO: automate which maps are available on each season
        self.m_params = importParams
        
        if importParams["data_spec"] == "all":
            self.m_rank = [str(i) for i in range(importParams["min_rank"], importParams["max_rank"]+1)]
            self.m_episode = [str(i) for i in range(importParams["min_episode"], importParams["max_episode"]+1)]
            self.m_act = [str(i) for i in range(importParams["min_act"], importParams["max_act"]+1)]
        else:
            self.m_rank = str(importParams["rank"])
            self.m_episode = str(importParams["episode"])
            self.m_act = str(importParams["act"])
            
    def fetch(self, url):
        response = requests.get(url)
        html = response.text
        return html
    
    def parse(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup
        
    def scrapeMaps(self):
        for rank in self.m_rank:
            for episode in self.m_episode:
                for act in self.m_act:
                    url = f"https://blitz.gg/valorant/stats/maps?sortBy=attackingRoundWinRate&sortDirection=DESC&mode=competitive&rank={rank}&act=e{episode}act{act}"
                    html = self.fetch(url)
                    soup = self.parse(html)
                    stats = soup.find_all("td", class_="Table-cell")
                    for stat in stats:
                        name = stat.find("div", class_="Table")
        
    def scrapeAgents(self):
        for rank in self.m_rank:
            for episode in self.m_episode:
                for act in self.m_act:
                    url = f"https://blitz.gg/valorant/stats/agents?sortBy=matches&type=general&sortDirection=DESC&mode=competitive&rank={rank}&act=e{episode}act{act}"
        
    
    def scrapeWeapons(self):
        for rank in self.m_rank:
            for episode in self.m_episode:
                for act in self.m_act:
                    url = f"https://blitz.gg/valorant/stats/weapons?sortBy=killsPerMatch&type=all&sortDirection=DESC&mode=competitive&rank={rank}&act=e{episode}act{act}"
        
    
    def runScraper(self):
        if self.m_params["dataset"] == "all":
            self.scrapeAgents()
            self.scrapeMaps()
            self.scrapeWeapons()
        elif self.m_params["dataset"] == "agents":
            self.scrapeAgents()
        elif self.m_params["dataset"] == "maps":
            self.scrapeMaps()
        elif self.m_params["dataset"] == "weapons":
            self.scrapeWeapons()