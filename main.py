import os
import requests
from flask_cors import CORS, cross_origin
from flask import Flask, redirect, request

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.after_request
def apply_text_only(response):
    response.headers["Content-Type"] = "text/plain"
    return response

@app.errorhandler(403)
def forbidden(e):
    return '403 forbidden'

@app.route('/')
def root():
  return redirect(os.environ['ROOT_URL'], code=302)

@app.route('/shorten')
@cross_origin()
def shorten_url():
  token = request.args.get("token")
  url = request.arg.get("url")
  if token == os.environ["SHORTY_TOKEN"]:
    resp = requests.post("https://shorty.ridgeback.cole.ws/api/link",
      headers={
        "Authorization": f"Bearer {token}"
      },
      json={
        "url": url
    })
    return resp.json()
  else:
    abort(403)

app.run(port=80, host="0.0.0.0")
