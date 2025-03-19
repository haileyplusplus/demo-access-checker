import datetime

from backend.config_loader import ConfigLoader
from backend.token_manager import TokenManager


class AccessChecker:
    def __init__(self, configs: ConfigLoader, token_manager: TokenManager):
        self.configs = configs
        self.token_manager = token_manager

    def verify_access(self, desired_profile: str):
        user = self.configs.get_users().get(self.token_manager.active_user())
        if not user:
            return 'No logged in user'
        user_tokens = self.token_manager.active_user_tokens()
        current_group_tokens = user_tokens.valid_tokens()
        user_groups = set(user['groups'])
        profile = self.configs.get_profiles().get(desired_profile)
        if not profile:
            return f'Profile {desired_profile} does not exist'
        necessary_resources = profile['resources']
        resource_status = {}
        for resource_name in necessary_resources:
            resource_status[resource_name] = {}
            resource = self.configs.get_resources().get(resource_name)
            if not resource:
                return f'Resource config error retrieving resource {resource_name}'
            resource_groups = set([x.removeprefix('group:') for x in resource['permissions']])
            permissions_ok = resource_groups & user_groups
            if permissions_ok:
                resource_status[resource_name].update({'membership_ok': True})
            else:
                # If a user doesn't have access to a group it will be impossible to get tokens for it, so the
                # token check automatically fails and details about it are moot.
                resource_status[resource_name].update(
                    {'membership_ok': False,
                     'needed_group_membership': list(resource_groups),
                     'tokens_ok': False
                     })
                continue
            current_token_group_names = set([x['group_name'] for x in current_group_tokens])
            expiring_soon = {}
            for item in current_group_tokens:
                time_until_expiry = item['time_until_expiry']
                print(f' time to expiry ', time_until_expiry, item['group_name'])
                if time_until_expiry < datetime.timedelta(hours=1):
                    minutes = round(time_until_expiry.total_seconds() / 60)
                    expiring_soon[item['group_name']] = f'{minutes} minutes'
            print(current_group_tokens, resource_groups)
            print(expiring_soon)
            tokens_ok = resource_groups & current_token_group_names
            if tokens_ok:
                resource_status[resource_name].update({'tokens_ok': True,
                                                       'expiring_soon': expiring_soon})
            else:
                # For a better user experience, only show groups where it's possible for them to get tokens.
                possible_token_groups = user_groups & resource_groups
                resource_status[resource_name].update(
                    {'tokens_ok': False, 'needed_token_membership': list(possible_token_groups)})
        return resource_status
