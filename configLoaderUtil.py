import yaml


class ConfigLoaderUtil:

    @staticmethod
    def load_yaml(yaml_file: str) -> dict[str, any]:
        """Returns python object constructed from parsed YAML file

        Args:
            yaml_file (str): File in YAML format

        Returns:
            dict[str, any]: Dictionary constructed from YAML file
        """
        file = open(yaml_file, 'r')
        return yaml.safe_load(file)
