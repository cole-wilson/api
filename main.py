import os
import qrcode
import requests
from io import BytesIO, StringIO
from PIL import Image
from flask_cors import CORS, cross_origin
from flask import Flask, redirect, request, send_file
from subprocess import Popen, PIPE, STDOUT
from collections import defaultdict

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def serve_image(pil_img):
    img_io = StringIO()
    pil_img.save("image.jpg")
    img_io.seek(0)
    return send_file("image.jpg", mimetype='image/jpeg')

@app.after_request
def apply_text_only(response):
    response.headers["Content-Type"] = "text/plain"
    return response

@app.errorhandler(405)
def forbidden(e): return '405 method not allowed'

@app.errorhandler(403)
def forbidden(e): return '403 forbidden'

@app.errorhandler(500)
def forbidden(e): return '500 error'

@app.errorhandler(404)
def forbidden(e): return '404 not found'

@app.route('/')
def root():
  return redirect(os.environ['ROOT_URL'], code=302)

@app.route('/jpeg')
def jpeg():
    url = request.args.get("url")
    fetch = requests.get(url, headers={"user-agent":"curl/7.84.0"}, stream=True)
    print(fetch.status_code)
    img = Image.open(fetch.raw)
    img = img.convert("RGB")
    return serve_image(img)

@app.route('/workouts')
def workouts():
    token = request.args.get("token")
    return '{"workouts":[{"name":"umm", "icon":"bike", "text":"some text"}]}'

@app.route('/shorten')
@cross_origin()
def shorten_url():
  token = request.args.get("token")
  url = request.args.get("url")
  domain = request.args.get("domain", "https://cole.ws/+")
  if token == os.environ["SHORTY_TOKEN"]:
    resp = requests.post("http://srv-captain--shorty/api/link",headers={"Authorization": f"Bearer {token}"},json={
        "url": url
    } if request.args.get("name", None) is None else {"url": url, "name": request.args.get("name", "")})
    try: return domain + resp.json()["data"]["name"]
    except: return resp.json()
  else:
    abort(403)

@app.route('/diagon', methods=["POST"])
@cross_origin()
def diagon():
    graph_type = request.args.get("type", "math").title()
    return requests.get("http://localhost:7642?type="+graph_type, data=request.get_data().decode()).content

@app.route('/qr')
@cross_origin()
def make_qr():
    background = request.args.get("bg", "white")
    foreground = request.args.get("fg", "black")
    inside = request.args.get("inside", None)
    size = request.args.get("size", 1)
    border = request.args.get("border", 1)
    data = request.args.get("data")
    error_correction = qrcode.constants.ERROR_CORRECT_L

    if inside is not None: error_correction = qrcode.constants.ERROR_CORRECT_H

    img = qrcode.make(data, version=size, error_correction=error_correction, box_size=10, border=border,)#fill_color=foreground, back_color=background)
    img = img.convert("RGBA")

    if inside is not None:
        w, h = round(0.25 * img.width), round(0.25 * img.height)
        brand = requests.get(inside)
        brand = Image.open(BytesIO(brand.content)).convert("RGBA")
        brand = brand.resize((w, h))
        xpos, ypos = (img.width - w)/2, (img.height - h)/2
        xpos, ypos = round(xpos), round(ypos)
        img.paste(brand, (xpos, ypos, xpos + w, ypos + h))

    return serve_image(img)

counts = defaultdict(int)

@app.route('/count')
@cross_origin()
def counter():
    global counts
    _id = request.args.get("i", "[default]")
    if "no" not in request.args:
        counts[_id] += 1
    return str(counts[_id])


app.run(port=80, host="0.0.0.0")
