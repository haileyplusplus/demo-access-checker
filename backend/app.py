from typing import Annotated

from fastapi import Cookie, FastAPI, HTTPException, Response

from backend.config_loader import ConfigLoader

app = FastAPI()
configs = ConfigLoader()


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
    if username not in configs.get_users():
        raise HTTPException(status_code=404, detail=f"User {username} not found.")
    response.set_cookie(key="user", value=username)
    return {'status': 'ok'}


@app.get('/get-user')
def get_user(user: Annotated[str | None, Cookie()] = None, profile: Annotated[str | None, Cookie()] = None):
    return {'user': user, 'profile': profile}


@app.get('/set-profile')
def set_profile(profile_name: str, response: Response):
    if profile_name not in configs.get_profiles():
        raise HTTPException(status_code=404, detail=f"Profile {profile_name} not found.")
    response.set_cookie(key="profile", value=profile_name)
    return {'status': 'ok'}


@app.get('/verify-access')
def verify_access(profile_name: str, user: Annotated[str | None, Cookie()] = None, profile: Annotated[str | None, Cookie()] = None):
    return {'verify_profile': profile_name,
            'user': user,
            'profile': profile}