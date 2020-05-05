import crcmod.predefined

from flask import render_template
from flask import jsonify
from flask import redirect
from flask import request
from app import app
from app.form import CrcForm

@app.route('/', methods=['GET'])
def create_form():
    crc_form = CrcForm()
    print(f"FORM ERRORS: {crc_form.errors}")
    return render_template('base.html', form=crc_form)

@app.route('/crc', methods=['POST'])
def generate_crc():
    crc_func = crcmod.predefined.mkCrcFun(request.values['crcType'])
    res = crc_func(bytes(request.values['inputData'], 'utf-8'))
    bit_str = f"{res:08b}"
    bit_str_8 = ' '.join([bit_str[i:i+8] for i in range(0, len(bit_str), 8)])
    return jsonify({
        "crc": bit_str_8,
        "realCrc": bit_str,
    })