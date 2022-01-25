import os
import qrcode
import requests
from io import BytesIO, StringIO
from PIL import Image
from flask_cors import CORS, cross_origin
from flask import Flask, redirect, request, send_file
from subprocess import Popen, PIPE, STDOUT

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def serve_image(pil_img):
    img_io = StringIO()
    pil_img.save("image.png")
    img_io.seek(0)
    return send_file("image.png", mimetype='image/jpeg')

@app.after_request
def apply_text_only(response):
    response.headers["Content-Type"] = "text/plain"
    return response

@app.errorhandler(403)
def forbidden(e): return '403 forbidden'

@app.errorhandler(500)
def forbidden(e): return '500 error'

@app.errorhandler(404)
def forbidden(e): return '404 not found'

@app.route('/')
def root():
  return redirect(os.environ['ROOT_URL'], code=302)

@app.route('/shorten')
@cross_origin()
def shorten_url():
  token = request.args.get("token")
  url = request.args.get("url")
  domain = request.args.get("domain", "https://cole.ws/+")
  if token == os.environ["SHORTY_TOKEN"]:
    resp = requests.post("http://srv-captain--shorty/api/link",headers={"Authorization": f"Bearer {token}"},json={
        "url": url
    })
    try: return domain + resp.json()["data"]["name"]
    except: return resp.json()
  else:
    abort(403)

@app.route('/diagon', methods=["GET"])
@cross_origin()
def diagon():
    return "POST"
    
@app.route('/diagon', methods=["POST"])
@cross_origin()
def diagon():
    graph_type = request.args.get("type", "math").title()
    style = request.args.get("style", "Unicode").title()
    p = Popen(['bin/diagon', graph_type, '-style='+style], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout_data = p.communicate(input=str(request.get_data(), 'utf-8'))[0]
    return stdout_data

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

    img = qrcode.make(data, version=size, error_correction=error_correction, box_size=10, border=border,)#fill_color=foreground, back_color=background
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

app.run(port=80, host="0.0.0.0")
    
    
    
