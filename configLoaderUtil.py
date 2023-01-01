import yaml

class ConfigLoaderUtil:
    
    @staticmethod
    def load_yaml(yaml_file):
        '''
        Returns python object constructed from parsed YAML file
        ---
        Inputs:
            yamlFile
                File in YAML format
        ---
        Outputs:
            Dictionary constructed from YAML file
        '''
        file = open(yaml_file, 'r')
        return yaml.safe_load(file)