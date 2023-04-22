from ConfigLoaderUtil import ConfigLoaderUtil
from BlitzScraper import BlitzScraper


def main()->None:
    # print(configLoaderUtil.loadYaml('config.yml'))
    config_params = ConfigLoaderUtil.load_yaml("config.yml")
    if config_params["run_mode"] == "load_data":
        scraper = BlitzScraper(config_params['data_import_parameters'])
        scraper.run_scraper()


if __name__ == "__main__":
    main()
