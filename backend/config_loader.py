import json
from pathlib import Path


class ConfigLoader:
    CONFIG_DIRECTORY = Path(__file__).parent.parent / 'config'

    def __init__(self):
        self.users = {}
        self.profiles = {}
        self.load_user_config()
        self.load_profile_config()

    def load_user_config(self):
        user_config = self.CONFIG_DIRECTORY / 'users.json'
        with user_config.open() as fh:
            config_users = json.load(fh)['users']
            for user in config_users:
                self.users[user['id']] = user

    def load_profile_config(self):
        profile_config = self.CONFIG_DIRECTORY / 'accessprofiles.json'
        with profile_config.open() as fh:
            config_profiles = json.load(fh)['profiles']
            for profile in config_profiles:
                id_ = profile['name']
                self.profiles[id_] = profile

    def get_users(self):
        return self.users

    def get_profiles(self):
        return self.profiles
