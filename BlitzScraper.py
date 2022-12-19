from selenium import webdriver
import os
import pandas as pd

class BlitzScraper:
    def __init__(self, path = None):
        # If no driver passed in then assumes driver is located on Desktop
        if path is None:
            path = os.path.expanduser('~/Desktop/chromedriver')
        self.driver = webdriver.Chrome(path)