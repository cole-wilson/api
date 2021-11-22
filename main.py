import os
import requests
from flask_cors import CORS, cross_origin
from flask import Flask, redirect, request

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def root():
  return redirect(os.environ['ROOT_URL'], code=302)

@app.route('/shorten')
@cross_origin()
def shorten_url():
  token = request.args.get("token")
  url = request.arg.get("url")
