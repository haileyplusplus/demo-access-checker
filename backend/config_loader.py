import json
from pathlib import Path


class ConfigLoader:
    CONFIG_DIRECTORY = Path(__file__).parent.parent / 'config'

    def __init__(self):
        self.users = {}
        self.profiles = {}
        self.groups = {}
        self.resources = {}
        self.load_user_config()
        self.load_profile_config()
        self.load_resource_config()
        self.load_group_config()

    def load_user_config(self):
        user_config = self.CONFIG_DIRECTORY / 'users.json'
        with user_config.open() as fh:
            user_config_json = json.load(fh)['users']
            for user in user_config_json:
                self.users[user['id']] = user

    def load_profile_config(self):
        profile_config = self.CONFIG_DIRECTORY / 'accessprofiles.json'
        with profile_config.open() as fh:
            profile_config_json = json.load(fh)['profiles']
            for profile in profile_config_json:
                id_ = profile['name']
                self.profiles[id_] = profile

    def load_group_config(self):
        group_config = self.CONFIG_DIRECTORY / 'groups.json'
        with group_config.open() as fh:
            group_config_json = json.load(fh)['groups']
            for group in group_config_json:
                id_ = group['name']
                self.groups[id_] = group

    def load_resource_config(self):
        resource_config = self.CONFIG_DIRECTORY / 'resources.json'
        with resource_config.open() as fh:
            resource_config_json = json.load(fh)['resources']
            for resource in resource_config_json:
                name = resource['name']
                self.resources[name] = resource

    def get_users(self):
        return self.users

    def get_profiles(self):
        return self.profiles

    def get_groups(self):
        return self.groups

    def get_resources(self):
        return self.resources
