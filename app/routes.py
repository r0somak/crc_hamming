from flask import render_template
from flask import jsonify
from flask import request
from flask import make_response

from app import app
from app.form import CrcForm
from app import hamming
from app.utils import generate_crc, zfill_crc

@app.route('/', methods=['GET'])
def create_form():
    crc_form = CrcForm()
    print(f"FORM ERRORS: {crc_form.errors}")
    return make_response(render_template('base.html', form=crc_form), 200)

@app.route('/hamming', methods=['POST'])
def generate_hamming():
    input_data = request.values['inputData']
    if len(input_data) < 10:
        return make_response(f"Input data has {len(input_data)} chars, minimum 10 required", 400)
    crc = generate_crc(request.values['inputData'], request.values['crcType'])
    crc = zfill_crc(crc)

    binput = "".join(f"{ord(i):08b}" for i in request.values['inputData'])
    #split bit string to 8bit chunks
    binput_8 = ' '.join([binput[i:i+8] for i in range(0, len(binput), 8)])

    inp_crc = binput + crc

    return make_response(jsonify({
        "crc": crc,
        "bitInputData": binput_8,
        "inp_crc": inp_crc,
        "hamming": hamming.encode(inp_crc),
    }), 200)

@app.route('/corrupt', methods=['POST'])
def corrupt_data():
    data = request.values['inputData']
    lst_data = list(data)
    positions = request.values['positions'].split(',')
    try:
        positions = [int(i.strip()) for i in positions]
    except ValueError as e:
        return make_response("Invalid input data", 400)
    positions.sort()
    if positions[-1] > len(data):
        return make_response(u"Last position exceeds input data length.", 400)
    lst_pos = list(positions)
    for i in range(len(lst_pos)):
        if lst_data[lst_pos[i]] == 1:
            lst_data[lst_pos[i]] = 0
        else:
            lst_data[lst_pos[i]] = 1
    lst_data = [str(i) for i in lst_data]
    new_data = ''.join(lst_data)
    print(positions)
    return make_response(jsonify({
        "corruptedData": new_data,
        "corruptedPositions": positions,
    }), 200)