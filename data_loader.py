import numpy as np
import pandas as pd
import pathlib


# Requirements
# Must be able to combine values that are specified and return modified csv
# Must be able to import CSV into pandas file and return it
class DataPipeline():
    def __init__(self) -> None:
        self.m_curr_dir = str(pathlib.Path.cwd())
        
        self.m_maps = ["split", "ascent", "haven", "icebox",
                       "breeze", "bind", "fracture", "pearl", "lotus"]

    def collect_file_params(self, 
                            load_params: dict[str, any] = None
                            )->tuple[list[int], list[int], list[int]]:
        if load_params["data_spec"] == "all":
            ranks = [i for i in range(
                load_params["min_rank"], load_params["max_rank"]+1)]
            episodes = [i for i in range(
                load_params["min_episode"], load_params["max_episode"]+1)]
            acts = [i for i in range(
                load_params["min_act"], load_params["max_act"]+1)]
        else:
            ranks = load_params["rank"]
            episodes = load_params["episode"]
            acts = load_params["act"]
        return ranks, episodes, acts

    def import_data(self, 
                    dataset: str = "Agents", 
                    load_params: dict[str, any] = None, 
                    agent_maps: bool = False
                    )->dict[str, pd.DataFrame]:
        # Requirements
        # Takes in multiple ranks, episodes, and acts
        # Stores them in dictionary where key is identifier and value is the imported dataframe
        dataframe_dict = {}

        ranks, episodes, acts = self.collect_file_params(load_params)

        for rank in ranks:
            for episode in episodes:
                for act in acts:
                    key = f"rank{rank}_episode{episode}_act{act}"
                    path = f"{self.m_curr_dir}/{dataset}/{dataset}_{key}"
                    self.load_csv(dataframe_dict, key, path, agent_maps)
        return dataframe_dict
    
    def load_csv(self, 
                 dataframe_dict: dict[str, pd.DataFrame], 
                 key: str, path: str, 
                 agent_maps: bool)->None:
        """_summary_

        Args:
            dataframe_dict (dict[str, pd.DataFrame]): _description_
            key (str): _description_
            path (str): _description_
            agent_maps (bool): _description_
        """
        if agent_maps:
            for map in self.m_maps:
                filename = f"{path}_map{map}.csv"
                try:
                    dataframe_dict[f"{key}_map{map}"] = pd.read_csv(filename, index_col=0)
                except FileNotFoundError:
                    print(f"DataPipeline::load_csv -- file {filename} does not exist")
                
        else:
            dataframe_dict[key] = pd.read_csv(f"{path}.csv")
