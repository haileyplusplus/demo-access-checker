import json
from pathlib import Path
from typing import Annotated

from fastapi import Cookie, FastAPI, HTTPException, Response


app = FastAPI()


LOCAL_DIRECTORY = Path(__file__).parent


def load_user_config():
    user_config = LOCAL_DIRECTORY.parent / 'config' / 'users.json'
    users_db = {}
    with user_config.open() as fh:
        users = json.load(fh)['users']
        for user in users:
            users_db[user['id']] = user
    return users_db


def load_profile_config():
    profile_config = LOCAL_DIRECTORY.parent / 'config' / 'accessprofiles.json'
    configured = {}
    with profile_config.open() as fh:
        profiles = json.load(fh)['profiles']
        for profile in profiles:
            id_ = profile['name']
            configured[id_] = profile
    return configured


users = load_user_config()
profiles = load_profile_config()


@app.get('/cookieset')
def cookie_set(arg: str, response: Response):
    #print(response.__dict__)
    response.set_cookie(key="user_scope", value=arg)
    return {'cookie':
            'set2'}


@app.get('/cookietest')
def cookie_test(user_scope: Annotated[str | None, Cookie()] = None):
    return {'cookie': user_scope}


@app.get('/set-user')
def set_user(username: str, response: Response):
    if username not in users:
        raise HTTPException(status_code=404, detail=f"User {username} not found.")
    response.set_cookie(key="user", value=username)
    return {'status': 'ok'}


@app.get('/get-user')
def get_user(user: Annotated[str | None, Cookie()] = None, profile: Annotated[str | None, Cookie()] = None):
    return {'user': user, 'profile': profile}


@app.get('/set-profile')
def set_profile(profile_name: str, response: Response):
    if profile_name not in profiles:
        raise HTTPException(status_code=404, detail=f"Profile {profile_name} not found.")
    response.set_cookie(key="profile", value=profile_name)
    return {'status': 'ok'}
