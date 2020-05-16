from flask import render_template
from flask import jsonify
from flask import redirect
from flask import request

from app import app
from app.form import CrcForm
from app import hamming
from app.utils import generate_crc, zfill_crc

@app.route('/', methods=['GET'])
def create_form():
    crc_form = CrcForm()
    print(f"FORM ERRORS: {crc_form.errors}")
    return render_template('base.html', form=crc_form)

@app.route('/hamming', methods=['POST'])
def generate_hamming():
    crc = generate_crc(request.values['inputData'], request.values['crcType'])
    crc = zfill_crc(crc)

    binput = "".join(f"{ord(i):08b}" for i in request.values['inputData'])
    #split bit string to 8bit chunks
    binput_8 = ' '.join([binput[i:i+8] for i in range(0, len(binput), 8)])

    inp_crc = binput + crc

    return jsonify({
        "crc": crc,
        "bitInputData": binput_8,
        "inp_crc": inp_crc,
        "hamming": hamming.encode(inp_crc),
    })
