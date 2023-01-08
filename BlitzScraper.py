import requests
from bs4 import BeautifulSoup
import pandas as pd


class BlitzScraper:
    def __init__(self, import_params):
        # TODO: automate which maps are available on each season
        self.m_params = import_params
        self.m_url_map = {
            "Agents": "https://blitz.gg/valorant/stats/agents?sortBy=matches&type=general&sortDirection=DESC&mode=competitive",
            "Maps": "https://blitz.gg/valorant/stats/maps?sortBy=attackingRoundWinRate&sortDirection=DESC&mode=competitive",
            "Weapons": "https://blitz.gg/valorant/stats/weapons?sortBy=killsPerMatch&type=all&sortDirection=DESC&mode=competitive"
        }

        if import_params["data_spec"] == "all":
            self.m_rank = [i for i in range(
                import_params["min_rank"], import_params["max_rank"]+1)]
            self.m_episode = [i for i in range(
                import_params["min_episode"], import_params["max_episode"]+1)]
            self.m_act = [i for i in range(
                import_params["min_act"], import_params["max_act"]+1)]
        else:
            self.m_rank = import_params["rank"]
            self.m_episode = import_params["episode"]
            self.m_act = import_params["act"]

    def fetch(self, url):
        response = requests.get(url)
        html = response.text
        return html

    def parse(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def extract_data(self, soup):
        data = []
        # Find the block containing the data table
        soup_main = soup.find("main")
        
        titles = self.extract_titles(soup_main)
        data = self.extract_row_data(soup_main)
        df = self.create_dataframe(data, titles)
        return df
    
    def extract_titles(self, soup_main):
        # Use a dictionary to check uniqueness and preserve order
        titles_list = {}
        # Titles on Blitz.gg are placed in a single row of height 30
        soup_main_titles = soup_main.find("div", height="30")
        
        # Separate out the titles after finding the titles row
        titles = soup_main_titles.find_all("div")
        for title in titles:
            # Ensure no empty strings are allowed
            if len(title.text) > 0:
                titles_list[title.text] = None
        titles_list = list(titles_list.keys())
        return titles_list
    
    def extract_row_data(self, soup_main):
        data = []
        # Data rows on Blitz.gg are placed in rows of height 48
        soup_main_row = soup_main.find_all("div", height="48")
        for row in soup_main_row:
            # Use a dictionary here to remove duplicates (list) and preserve order (set)
            row_data = {}
            # Separate out each column in the row
            row_div = row.find_all("div")
            for value in row_div:
                # Ensure no empty strings are allowed
                if len(value.text) > 0:
                    row_data[value.text] = None
            data.append(list(row_data.keys()))
        return data
    
    def scrape(self, url):
        html = self.fetch(url)
        soup = self.parse(html)
        data = self.extract_data(soup)
        return data

    def create_dataframe(self, data, column_names):
        df = pd.DataFrame(data, columns=column_names)
        return df

    def get_maps(self):
        self.m_season = {}
        for episode in self.m_episode:
            for act in self.m_act:
                # TODO: need this to get all map names
                self.m_maps[f"e{episode}act{act}"] = 0

    def perform_scrape(self, category):
        print(f"BlitzScraper::scrape_{category} -- collecting {category} data")
        
        # TODO: make this work with the df returned from scrape
        if self.m_params["data_spec"] == "all":
            for rank in self.m_rank:
                for episode in self.m_episode:
                    for act in self.m_act:
                        # print(f"Scraping::{category}_rank{rank}_episode{episode}_act{act}")
                        url = f"{self.m_url_map[category]}&rank={rank}&act=e{episode}act{act}"
                        try:
                            page_data = self.scrape(url)
                            page_data.to_csv(f"{category}/{category}_rank{rank}_episode{episode}_act{act}")
                        except:
                            print(f"Invalid Dataset Request::rank{rank}_episode{episode}_act{act}")
        else:
            # print(f"Scraping::{category}_rank{self.m_rank}_episode{self.m_episode}_act{self.m_act}")
            url = f"{self.m_url_map[category]}&rank={self.m_rank}&act=e{self.m_episode}act{self.m_act}"
            try:
                page_data = self.scrape(url)
                page_data.to_csv(f"{category}/{category}_rank{self.m_rank}_episode{self.m_episode}_act{self.m_act}")
            except:
                print(f"Invalid Dataset Request::rank{self.m_rank}_episode{self.m_episode}_act{self.m_act}")

    def run_scraper(self):
        print("BlitzScraper::run_scraper -- running scraper")

        if self.m_params["dataset"] == "all":
            self.perform_scrape("Weapons")
            self.perform_scrape("Maps")
            self.perform_scrape("Agents")
        else:
            self.perform_scrape(self.m_params["dataset"])
