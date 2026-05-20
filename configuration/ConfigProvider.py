import configparser

global_config = configparser.ConfigParser()
global_config.read('config.ini')


class ConfigProvider:

    def __init__(self) -> None:
        self.config = global_config

    def get(self, section: str, prop: str):
        return self.config[section].get(prop)

    def get_int(self, section: str, prop: str) -> int:
        return self.config[section].getint(prop)

    def get_ui_url(self) -> str:
        return self.config['ui'].get('base_url')

    def get_api_url(self) -> str:
        return self.config['api'].get('base_url')
