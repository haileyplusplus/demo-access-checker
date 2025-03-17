from fastapi import FastAPI

app = FastAPI()


@app.get('/status')
def status():
    return {'version': 1.0}


@app.get('/login')
def login():
    pass

