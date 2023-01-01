from ConfigLoaderUtil import ConfigLoaderUtil
import time
import os
from BlitzScraper import BlitzScraper

def main():
    # print(configLoaderUtil.loadYaml('config.yml'))
    config_params = ConfigLoaderUtil.load_yaml("config.yml")
    if config_params["run_mode"] == "load_data":
        scraper = BlitzScraper(config_params['data_import_parameters'])
        scraper.run_scraper()




if __name__ == "__main__":
    main()
