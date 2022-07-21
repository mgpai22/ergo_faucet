from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import main

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['POST'])
def my_form_post():
    address = request.form['address']
    try:
        tx = f'https://testnet.ergoplatform.com/en/transactions/{main.getERG(address)}'
    except Exception as e:
        tx = "Error"
    return tx
