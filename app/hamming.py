import numpy as np

def encode(data:str) -> str:
    '''
    Applies Hamming encoding to given bit string.
    '''
    lst_bin_data = [int(x) for x in data]
    bit_count = len(lst_bin_data)
    control_bits = [(1 << i)-1 for i in range(bit_count) if (1 << i) <= bit_count]
    cntrl_len = len(control_bits)
    schema = lst_bin_data
    for i in control_bits:
        schema.insert(i, None)
    one_pos = []
    for i in range(len(schema)):
        if schema[i] == 1:
            bits = format(i+1, 'b')
            if len(bits) < cntrl_len:
                bits = bits.zfill(cntrl_len)
            one_pos.append([int(b) for b in bits])
    one_pos.reverse()
    a = np.array(one_pos)
    control_bits.reverse()
    for i in range(cntrl_len):
        if np.sum(a[:,i]) % 2 == 0:
            schema[control_bits[i]] = 0
        else:
            schema[control_bits[i]] = 1
    return (control_bits, ''.join(map(str, schema)))

def fix(data:str) -> str:
    lst_bin_data = [int(x) for x in data]
    bit_count = len(lst_bin_data)
    one_pos = []
    control_bits = [(1 << i)-1 for i in range(bit_count) if (1 << i) <= bit_count]
    cntrl_len = len(control_bits)
    for i in range(bit_count):
        if lst_bin_data[i] == 1:
            bits = format(i+1, 'b')
            if len(bits) < cntrl_len:
                bits = bits.zfill(cntrl_len)
            one_pos.append([int(b) for b in bits])
    one_pos.sort()
    a = np.array(one_pos)
    parity_bits = []
    for i in range(cntrl_len):
        if np.sum(a[:,i]) % 2 == 0:
            parity_bits.append(0)
        else:
            parity_bits.append(1)
    parity_str = ''.join(map(str, parity_bits))
    pos_number = int(parity_str, 2) - 1
    if pos_number < 0:
        return (None, data)
    if lst_bin_data[pos_number] == 0:
        lst_bin_data[pos_number] = 1
    else:
        lst_bin_data[pos_number] = 0
    fixed_str = ''.join(map(str, lst_bin_data))
    return (pos_number, fixed_str)