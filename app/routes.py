import crcmod.predefined

from flask import render_template
from flask import jsonify
from flask import redirect
from flask import request
from app import app
from app.form import CrcForm
from app import hamming

@app.route('/', methods=['GET'])
def create_form():
    crc_form = CrcForm()
    print(f"FORM ERRORS: {crc_form.errors}")
    return render_template('base.html', form=crc_form)

@app.route('/crc', methods=['POST'])
def generate_crc():
    crc_func = crcmod.predefined.mkCrcFun(request.values['crcType'])
    bit_input = bytes(request.values['inputData'], 'utf-8')
    res = crc_func(bit_input)

    bit_str = f"{res:08b}"
    rbit_str = bit_str[::-1]
    rbit_str = ''.join([rbit_str[i:i+8].ljust(8, '0') for i in range(0, len(rbit_str), 8)])
    bit_str = rbit_str[::-1]


    binput = "".join(f"{ord(i):08b}" for i in request.values['inputData'])
    binput_8 = ' '.join([binput[i:i+8] for i in range(0, len(binput), 8)])

    inp_crc = binput + bit_str

    return jsonify({
        "crc": bit_str,
        "bitInputData": binput_8,
        "inp_crc": inp_crc,
        "hamming": hamming.encode(inp_crc)
    })
