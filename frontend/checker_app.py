from flask import Flask, render_template, request, abort, redirect
import requests


app = Flask(__name__)


BACKEND = 'http://backend:8099'


@app.route('/')
def main():
    profiles = requests.get(f'{BACKEND}/get-access-profiles')
    if profiles.status_code != 200:
        abort(profiles.status_code)
    return render_template("checker.html", profiles=profiles.json()['profiles'])


@app.route('/choose-environment', methods=['POST'])
def choose_environment():
    # A more polished app would make concurrent asynchronous requests to the backend.
    desired_profile = request.form.get('envprofile')
    if not desired_profile:
        abort(404)
    profiles = requests.get(f'{BACKEND}/get-access-profiles')
    if profiles.status_code != 200:
        abort(profiles.status_code)
    access_check = requests.get(f'{BACKEND}/verify-access', params={'desired_profile': desired_profile})
    if access_check.status_code != 200:
        abort(access_check.status_code)
    all_ok = True
    access_dict = access_check.json()
    if not access_dict['status']:
        abort(404)
    for k, v in access_dict['status'].items():
        if not v['membership_ok'] or not v['tokens_ok']:
            all_ok = False
    return render_template("checker.html",
                           profiles=profiles.json()['profiles'],
                           access=access_dict,
                           all_ok=all_ok
                           )


@app.route('/switch-profile')
def switch_profile():
    return render_template("profile_switcher.html", switch_to=request.args.get('switch_to'))


@app.route('/request-tokens')
def request_tokens():
    return render_template("request_tokens.html",
                           desired_profile=request.args.get('desired_profile'),
                           group=request.args.get('group'))


@app.route('/admin')
def admin():
    scenarios_req = requests.get(f'{BACKEND}/scenarios')
    if scenarios_req.status_code != 200:
        abort(scenarios_req.status_code)
    scenarios = scenarios_req.json()
    return render_template("scenarios.html", **scenarios)


@app.route('/set-scenario', methods=['POST'])
def set_scenario():
    scenarios_req = requests.post(f'{BACKEND}/test-scenario',
                                  params={'scenario_number': request.form.get('scenario')})
    if scenarios_req.status_code != 200:
        abort(scenarios_req.status_code)
    return redirect('/admin')
