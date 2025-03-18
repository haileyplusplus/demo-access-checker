import datetime


class UserTokens:
    def __init__(self, user_name: str):
        self.user_name = user_name
        self.tokens = {}
        self.profile = None

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


class TokenManager:
    def __init__(self):
        self.user_tokens = {}
        self.current_user = None

    def set_scenario(self, scenario):
        now = datetime.datetime.now(tz=datetime.UTC)
        user_name = scenario['user_name']
        self.current_user = user_name
        user_tokens = self.user_tokens.setdefault(user_name, UserTokens(user_name))
        profile_name, delta = scenario['profile']
        user_tokens.switch_profile(profile_name, now - delta)
        for token in scenario['tokens']:
            group_name, delta = token
            user_tokens.refresh_group_token(group_name, now - delta)

    def active_user(self):
        pass
