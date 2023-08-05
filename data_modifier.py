import pandas as pd
import numpy as np

class DataModifier():
    
    def add_roles(self, data: pd.DataFrame) -> pd.DataFrame:
        roles = []
        for agent in data['Agent ']:
            roles.append(self.agent_to_role[agent])
        data['Roles '] = roles
        return data
        
    def add_roles_all(self, dataset: dict[str, pd.DataFrame]):
        for data_key in dataset:
            dataset[data_key] = self.add_roles(dataset[data_key])
        return dataset
        
    def save_all_csv(self, data_type: str, dataset: dict[str, pd.DataFrame]):
        for data_key in dataset:
            dataset[data_key].to_csv(f'{data_type.capitalize()}/{data_type.capitalize()}_{data_key}.csv')
    
    
    agent_to_role: dict[str, str] = {
        'Raze': 'Duelist',
        'Jett': 'Duelist',
        'Phoenix': 'Duelist',
        'Yoru': 'Duelist',
        'Neon': 'Duelist',
        'Sage': 'Sentinel',
        'Omen': 'Controller',
        'Skye': 'Initiator',
        'Reyna': 'Duelist',
        'Killjoy': 'Sentinel',
        'Cypher': 'Sentinel',
        'Astra': 'Controller',
        'Breach': 'Initiator',
        'Brimstone': 'Controller',
        'KAY/O': 'Initiator',
        'Fade': 'Initiator',
        'Chamber': 'Sentinel',
        'Viper': 'Controller',
        'Sova': 'Initiator',
        'Harbor': 'Controller',
        'Gekko': 'Initiator',
        'Deadlock': 'Sentinel'
    }