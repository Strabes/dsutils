import yaml

class Configs():
    """
    Class to house configurations
    """
    def __init__(self,config_file_name):
        self.configs = self._load_config_file(config_file_name)
        
    def _load_config_file(self,config_file_name):
        with open(config_file_name,'r') as f:
            configs = yaml.safe_load(f)
        return(configs)