from flask import Flask, render_template, request, abort
import requests


app = Flask(__name__)


BACKEND = 'http://localhost:8000'


@app.route('/')
def main():
    profiles = requests.get(f'{BACKEND}/get-access-profiles')
    if profiles.status_code != 200:
        abort(profiles.status_code)
    return render_template("checker.html", profiles=profiles.json()['profiles'])


@app.route('/choose-environment', methods=['POST'])
def choose_environment():
    args = request.form
    return f'Submittedn: {args}'
