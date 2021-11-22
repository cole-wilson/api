import os
import qrcode
import requests
from io import BytesIO, StringIO
from flask_cors import CORS, cross_origin
from flask import Flask, redirect, request

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def serve_image(pil_img):
    img_io = StringIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

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
  if token == os.environ["SHORTY_TOKEN"]:
    resp = requests.post("http://srv-captain--shorty/api/link",headers={"Authorization": f"Bearer {token}"},json={
        "url": url
    })
    try: return "https://cole.ws/+" + resp.json()["data"]["name"]
    except: return resp.json()
  else:
    abort(403)

@app.route('/qr')
@cross_origin()
def make_qr():
    background = request.args.get("bg", "white")
    foreground = request.args.get("fg", "black")
    inside = request.args.get("inside", None)
    size = request.args.get("size", 20)
    border = request.args.get("border", 2)
    data = request.args.get("data")
    error_correction = qrcode.constants.ERROR_CORRECT_L
    
    if inside is not None: error_correction = qrcode.constants.ERROR_CORRECT_H

    qr = qrcode.QRCode(version=size, error_correction=error_correction, box_size=10, border=border,)#fill_color=foreground, back_color=background
    qr.add_data(data)
    img = qr.make()
    
    if inside is not None:
        w, h = round(0.25 * img.width), round(0.25 * img.height)
        brand = requests.get(inside)
        brand = Image.open(BytesIO(brand.content))
        brand = brand.resize((w, h))
        xmin = ymin = int((width / 2) - (logo_size / 2))
        xmax = ymax = int((width / 2) + (logo_size / 2))
        img.paste(brand, (xmin, ymin, xmax, ymax))
        
    return str(img)

app.run(port=80, host="0.0.0.0")
    
    
    
