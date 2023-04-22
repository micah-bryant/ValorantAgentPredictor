import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import OrderedDict


class BlitzScraper:
    def __init__(self, import_params: dict[str, any]) -> None:
        """Initializes the web scraper with correct urls, ranks to scrape, episodes to scrape, and acts to scrape

        Args:
            import_params (dict[str, any]): dictionary created from data import parameters in yaml file
        """
        self.m_params = import_params

        # Allocate base URLs to pass to requests in fstring
        self.m_url_map = {
            "Agents": "https://blitz.gg/valorant/stats/agents?sortBy=matches&type=general&sortDirection=DESC&mode=competitive",
            "Maps": "https://blitz.gg/valorant/stats/maps?sortBy=attackingRoundWinRate&sortDirection=DESC&mode=competitive",
            "Weapons": "https://blitz.gg/valorant/stats/weapons?sortBy=killsPerMatch&type=all&sortDirection=DESC&mode=competitive"
        }

        # Create ranks, episodes, and acts to scrape
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

    def fetch(self, url: str) -> str:
        """Attempts to fetch html file from url

        Args:
            url (str): a url that requests will attempt to access

        Returns:
            html (str): a string containing the entire html file response from requests in unicode
        """
        response = requests.get(url)
        html = response.text
        return html

    def parse(self, html: str) -> BeautifulSoup:
        """Generates beautifulsoup object that is able to be parsed by html keys

        Args:
            html (str): string object containing html file in unicode

        Returns:
            BeautifulSoup object: Object from an html file that can be parsed by html keys
        """
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def extract_data(self, soup: BeautifulSoup) -> pd.DataFrame:
        """Generated a pandas dataframe from data contained within a soup object

        Args:
            soup (BeautifulSoup object): object that contains an html file that is able to be parsed

        Returns:
            Pandas dataframe: dataframe containing data from the soup object
        """
        data = []
        # Find the block containing the data table
        soup_main = soup.find("main")

        titles = self.extract_titles(soup_main)
        data = self.extract_row_data(soup_main)
        df = self.create_dataframe(data, titles)
        return df

    def extract_titles(self, soup_main: BeautifulSoup) -> list[str]:
        """Extract the title strings from soup object

        Args:
            soup_main (BeautifulSoup object): soup object parsed by main tag

        Returns:
            list[str]: a list of titles for columns in a dataframe
        """
        # Use ordered dictionary to check uniqueness and preserve order of being added
        titles_list = OrderedDict()
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

    def extract_row_data(self, soup_main: BeautifulSoup) -> list[list[str]]:
        """Extract the data from soup object

        Args:
            soup_main (BeautifulSoup object): soup object parsed by main tag

        Returns:
            list[list[str]]: a list of lists of row data
        """
        data = []
        # Data rows on Blitz.gg are placed in rows of height 48
        soup_main_row = soup_main.find_all("div", height="48")
        for row in soup_main_row:
            # Use ordered dictionary here to remove duplicates (list) and preserve order (set)
            row_data = OrderedDict()
            # Separate out each column in the row
            row_div = row.find_all("div")
            for value in row_div:
                # Ensure no empty strings are allowed
                if len(value.text) > 0:
                    row_data[value.text] = None
            data.append(list(row_data.keys()))
        return data

    def scrape(self, url: str) -> pd.DataFrame:
        """Scrape the URL for the data in a table and return in pandas dataframe

        Args:
            url (str): URL containing the data to be scraped

        Returns:
            pandas dataframe: dataframe containing the data found within the URL
        """
        html = self.fetch(url)
        soup = self.parse(html)
        data = self.extract_data(soup)
        return data

    def create_dataframe(self, data:list[list[str]], column_names:list[str])->pd.DataFrame:
        """Create a pandas dataframe based on the data and label the columns

        Args:
            data (list[list[str]]): list of lists containg row data
            column_names (list[str]): list of strings containing column titles

        Returns:
            pandas dataframe: dataframe constructed from passed in data and column titles
        """
        df = pd.DataFrame(data, columns=column_names)
        return df

    def perform_scrape(self, category:str)->None:
        """Scrape Blitz.gg for data based on category, rank, episode, and act
            Save it to appropriate folder based on category, create a CSV, and label it

        Args:
            category (str): string declaring whether to scrape Maps, Agents, or Weapons
        """
        print(f"BlitzScraper::perform_scrape -- collecting {category} data")

        if self.m_params["data_spec"] == "all":
            for rank in self.m_rank:
                for episode in self.m_episode:
                    for act in self.m_act:
                        url = f"{self.m_url_map[category]}&rank={rank}&act=e{episode}act{act}"
                        try:
                            page_data = self.scrape(url)
                            page_data.to_csv(
                                f"{category}/{category}_rank{rank}_episode{episode}_act{act}.csv")
                        except:
                            print(
                                f"Invalid Dataset Request::rank{rank}_episode{episode}_act{act}")
        else:
            url = f"{self.m_url_map[category]}&rank={self.m_rank}&act=e{self.m_episode}act{self.m_act}"
            try:
                page_data = self.scrape(url)
                page_data.to_csv(
                    f"{category}/{category}_rank{self.m_rank}_episode{self.m_episode}_act{self.m_act}.csv")
            except:
                print(
                    f"Invalid Dataset Request::rank{self.m_rank}_episode{self.m_episode}_act{self.m_act}")

    def run_scraper(self)->None:
        """Run webscraper for Blitz.gg based on yaml config parameters"""
        print("BlitzScraper::run_scraper -- running scraper")

        if self.m_params["dataset"] == "all":
            self.perform_scrape("Weapons")
            self.perform_scrape("Maps")
            self.perform_scrape("Agents")
        else:
            self.perform_scrape(self.m_params["dataset"])
