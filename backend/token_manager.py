import datetime

from backend.config_loader import ConfigLoader


class UserTokens:
    def __init__(self, configs, user_name: str):
        self.user_name = user_name
        self.tokens = {}
        self.profile = None
        self.configs = configs

    def switch_profile(self, profile_name, timestamp: datetime.datetime):
        """
        Only one given profile can be active at any given time. If tokens
        have expired for the most recently requested profile, no profile
        is active.
        :return:
        """
        self.profile = (profile_name, timestamp)

    def refresh_group_token(self, group_name, timestamp: datetime.datetime):
        self.tokens[group_name] = timestamp

    def valid_tokens(self):
        now = datetime.datetime.now(tz=datetime.UTC)
        groups = []
        for group_name, timestamp in self.tokens.items():
            token_valid_hours = self.configs.get_groups()[group_name]['token_hours']
            expires: datetime.datetime = timestamp + datetime.timedelta(hours=token_valid_hours)
            if expires >= now:
                time_until_expiry = expires - now
                groups.append({
                    'group_name': group_name,
                    'time_until_expiry': time_until_expiry
                })
        return groups


class TokenManager:
    def __init__(self, configs: ConfigLoader):
        self.user_tokens = {}
        self.current_user = None
        self.configs = configs
        self.current_scenario = None

    def set_scenario(self, scenario):
        self.current_scenario = scenario
        now = datetime.datetime.now(tz=datetime.UTC)
        user_name = scenario['user_name']
        self.current_user = user_name
        user_tokens = self.user_tokens.setdefault(user_name, UserTokens(self.configs, user_name))
        profile_name, delta = scenario['profile']
        user_tokens.switch_profile(profile_name, now - delta)
        for token in scenario['tokens']:
            group_name, delta = token
            user_tokens.refresh_group_token(group_name, now - delta)

    def active_user(self):
        return self.current_user

    def active_user_tokens(self):
        if self.current_user is None:
            return None
        return self.user_tokens[self.current_user]

    def active_profile(self):
        now = datetime.datetime.now(tz=datetime.UTC)
        if self.current_user is None:
            return None
        profile_name, timestamp = self.user_tokens[self.current_user].profile
        profile = self.configs.get_profiles().get(profile_name)
        if not profile:
            return None
        expires = timestamp + datetime.timedelta(hours=profile['token_hours'])
        if now > expires:
            return None
        return profile_name
