from backend.config_loader import ConfigLoader


class AccessChecker:
    def __init__(self):
        self.configs = ConfigLoader()

    def verify_access(self, profile_name: str, user_name: str):
        user = self.configs.get_users().get(user_name)
        if not user:
            return 'User does not exist'
        user_groups = set(user['groups'])
        profile = self.configs.get_profiles().get(profile_name)
        if not profile:
            return 'Profile does not exist'
        necessary_resources = profile['resources']
        resource_status = {}
        for resource_name in necessary_resources:
            resource = self.configs.get_resources().get(resource_name)
            if not resource:
                return f'Resource config error retrieving resource {resource_name}'
            resource_groups = set([x.removeprefix('group:') for x in resource['permissions']])
            permissions_ok = resource_groups & user_groups
            if permissions_ok:
                resource_status[resource_name] = {'ok': True}
            else:
                resource_status[resource_name] = {'ok': False, 'needed_group': list(resource_groups)}
        return resource_status
