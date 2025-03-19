import datetime

from fastapi import FastAPI, HTTPException

from backend.access_checker import AccessChecker
from backend.config_loader import ConfigLoader
from backend.token_manager import TokenManager


class State:
    def __init__(self):
        self.configs = ConfigLoader()
        self.token_manager = TokenManager(self.configs)
        self.access_checker = AccessChecker(
            configs=self.configs, token_manager=self.token_manager)


app = FastAPI()
state = State()


@app.get('/verify-access')
def verify_access(desired_profile: str):
    checker = state.access_checker
    status = checker.verify_access(desired_profile)
    active_profile = state.token_manager.active_profile()
    profile_match = desired_profile == active_profile
    return {'desired_profile': desired_profile,
            'current_profile': active_profile,
            'profile_match': profile_match,
            'user': state.token_manager.active_user(),
            'status': status}


@app.get('/get-access-profiles')
def get_access_profiles():
    profiles = []
    for k, v in state.configs.get_profiles().items():
        profiles.append({'profile_name': k, 'description': v['description']})
    return {'profiles': profiles}


@app.post('/test-scenario')
def test_scenario(scenario_number: int):
    scenarios = [
        # Missing resources
        {'scenario_name': 'Missing resources',
         'user_name': 'daisy@example.com',
         'profile':
             ('greenlight-dev', datetime.timedelta(hours=100)),
         'tokens':
            [('greenlight-dev', datetime.timedelta(hours=20))]
         },
        # All resources present for greenlight-prod
        {'scenario_name': 'All resources present for greenlight-prod',
         'profile':
             ('greenlight-prod', datetime.timedelta(hours=7)),
         'tokens':
            [
                ('greenlight-vpn', datetime.timedelta(hours=100)),
                ('greenlight-dev', datetime.timedelta(hours=50)),
                ('greenlight-oncall', datetime.timedelta(hours=8))
            ],
         'user_name': 'daisy@example.com'},
        # Expired profile
        {'scenario_name': 'Expired profile',
         'profile':
             ('greenlight-prod', datetime.timedelta(hours=18)),
         'tokens':
             [
                 ('greenlight-vpn', datetime.timedelta(hours=100)),
                 ('greenlight-dev', datetime.timedelta(hours=50)),
                 ('greenlight-oncall', datetime.timedelta(hours=8))
             ],
         'user_name': 'daisy@example.com'},
        # Some expired tokens
        {'scenario_name': 'Some expired tokens',
         'profile':
             ('greenlight-prod', datetime.timedelta(hours=7)),
         'tokens':
             [
                 ('greenlight-vpn', datetime.timedelta(hours=100)),
                 ('greenlight-dev', datetime.timedelta(hours=200)),
                 ('greenlight-oncall', datetime.timedelta(hours=14))
             ],
         'user_name': 'daisy@example.com'},
        # Group membership missing
        {'scenario_name': 'Group membership missing',
         'profile':
             ('oxford-dev', datetime.timedelta(hours=7)),
         'tokens':
             [
                 ('oxford-dev', datetime.timedelta(hours=200)),
             ],
         'user_name': 'gatsby@example.com'},
        # Resources present for greenlight-prod but tokens expire soon
        {'scenario_name': 'Resources present for greenlight-prod but tokens expire soon',
         'profile':
             ('greenlight-prod', datetime.timedelta(hours=7)),
         'tokens':
             [
                 ('greenlight-vpn', datetime.timedelta(hours=100)),
                 ('greenlight-dev', datetime.timedelta(hours=50)),
                 ('greenlight-oncall', datetime.timedelta(hours=11, minutes=45))
             ],
         'user_name': 'daisy@example.com'},
    ]
    """
    Choose among various imagined states of user login and requested resources for testing
    """
    if scenario_number < 0 or scenario_number >= len(scenarios):
        raise HTTPException(status_code=404, detail=f"Scenario {scenario_number} not found.")
    state.token_manager.set_scenario(scenarios[scenario_number])
    return {'status': 'ok'}


# Always load a testing scenario on startup so we're never in an invalid state.
test_scenario(5)
