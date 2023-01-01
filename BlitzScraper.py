import requests
from bs4 import BeautifulSoup
import pandas as pd

class BlitzScraper:
    def __init__(self, import_params):
        # TODO: automate which maps are available on each season
        self.m_params = import_params
        
        if import_params["data_spec"] == "all":
            self.m_rank = [str(i) for i in range(import_params["min_rank"], import_params["max_rank"]+1)]
            self.m_episode = [str(i) for i in range(import_params["min_episode"], import_params["max_episode"]+1)]
            self.m_act = [str(i) for i in range(import_params["min_act"], import_params["max_act"]+1)]
        else:
            self.m_rank = str(import_params["rank"])
            self.m_episode = str(import_params["episode"])
            self.m_act = str(import_params["act"])
            
    def fetch(self, url):
        response = requests.get(url)
        html = response.text
        return html
    
    def parse(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup
    
    def extract_data(self, soup):
        data = []
        stats = soup.find_all("td", class_="Table-cell")
        for stat in stats:
            name = stat.find("div", class_="Table")
            value = stat.find("div", class_="Table-rowValue").text
            data.append([name, value])
        return data
    
    def create_dataframe(self, data, column_names = ["Name", "Value"]):
        df = pd.DataFrame(data, columns=column_names)
        return df
        
    def get_maps(self):
        self.m_season = {}
        for episode in self.m_episode:
            for act in self.m_act:
                # TODO: need this to get all map names
                self.m_maps[f"e{episode}act{act}"] = 0
        
    def scrape_maps(self):
        print("BlitzScraper::scrape_maps -- collecting map data")
        data = []
        for rank in self.m_rank:
            for episode in self.m_episode:
                for act in self.m_act:
                    url = f"https://blitz.gg/valorant/stats/maps?sortBy=attackingRoundWinRate&sortDirection=DESC&mode=competitive&rank={rank}&act=e{episode}act{act}"
                    html = self.fetch(url)
                    soup = self.parse(html)
                    page_data = self.extract_data(soup)
                    print(type(html))
                    print(type(soup))
                    data.extend(page_data)
        df = self.create_dataframe(data)
        return df
                    
                    
        
    def scrape_agents(self):
        for rank in self.m_rank:
            for episode in self.m_episode:
                for act in self.m_act:
                    url = f"https://blitz.gg/valorant/stats/agents?sortBy=matches&type=general&sortDirection=DESC&mode=competitive&rank={rank}&act=e{episode}act{act}"
        
    
    def scrape_weapons(self):
        for rank in self.m_rank:
            for episode in self.m_episode:
                for act in self.m_act:
                    url = f"https://blitz.gg/valorant/stats/weapons?sortBy=killsPerMatch&type=all&sortDirection=DESC&mode=competitive&rank={rank}&act=e{episode}act{act}"
        
    
    def run_scraper(self):
        print("BlitzScraper::run_scraper -- running scraper")

        if self.m_params["dataset"] == "all":
            self.scrape_agents()
            self.scrape_maps()
            self.scrape_weapons()
        elif self.m_params["dataset"] == "agents":
            self.scrape_agents()
        elif self.m_params["dataset"] == "maps":
            df = self.scrape_maps()
            print(df)
        elif self.m_params["dataset"] == "weapons":
            self.scrape_weapons()