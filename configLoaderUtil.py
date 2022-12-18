import yaml

class configLoaderUtil:
    
    @staticmethod
    def loadYaml(yamlFile):
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
        file = open(yamlFile, 'r')
        return yaml.safe_load(file)