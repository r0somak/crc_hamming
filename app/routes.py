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
    control_bits, output = hamming.encode(inp_crc)
    return make_response(jsonify({
        "crc": crc,
        "bitInputData": binput_8,
        "inp_crc": inp_crc,
        "hamming": output,
        "ctrl_pos": control_bits,
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
    for i in positions:
        if lst_data[i] == '1':
            lst_data[i] = '0'
        else:
            lst_data[i] = '1'
    new_data = ''.join(lst_data)
    return make_response(jsonify({
        "corruptedData": new_data,
        "corruptedPositions": positions,
    }), 200)

@app.route('/fix', methods=['POST'])
def fix_data():
    data = request.values['inputData']
    cor_pos, output = hamming.fix(data)
    return make_response(jsonify({
        "corPos": cor_pos,
        "output": output,
    }), 200)


@app.route('/decode', methods=['POST'])
def decode_data():
    data = list(request.values['inputData'])
    ctrl_pos = [(1 << i)-1 for i in range(len(data)) if (1 << i) <= len(data)]
    crc = request.values['crc_code']
    original = request.values['original_data']
    original = original.replace(' ', '')
    for i in ctrl_pos:
        data[i] = 'd'
    data = ''.join(data)
    data = data.replace('d', '')

    data = data[0:-len(crc)]
    if original == data:
        message = "Success in decoding data"
    else:
        message = "Failure in decoding data"
    data_8 = ' '.join([data[i:i+8] for i in range(0, len(data), 8)])
    bin_val = data_8.split()
    ascii_string = ""
    for binary in bin_val:
        inti = int(binary, 2)
        char = chr(inti)
        ascii_string += char
    
    return make_response(jsonify({
        "data": data,
        "original": original,
        "msg": message,
        "ascii": ascii_string
    }), 200)