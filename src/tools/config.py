import json
from settings import SETTINGS as settings


class ConfigManager:
    @staticmethod
    def get_config() -> dict:
        with open(settings.CONFIG_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def update_config(new_data: dict) -> None:
        with open(settings.CONFIG_PATH, 'r', encoding='utf-8') as file:
            config = json.load(file)

        config.update(new_data)

        with open(settings.CONFIG_PATH, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4, ensure_ascii=False)