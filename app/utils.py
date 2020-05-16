import crcmod.predefined

def generate_crc(data:str, crc_type:str, encoding='utf-8') -> str:
    '''
    Generates CRC from given data input.
    For available crc_type visit http://crcmod.sourceforge.net/crcmod.predefined.html.
    '''
    crc_func = crcmod.predefined.mkCrcFun(crc_type)
    bit_input = bytes(data, encoding)
    return crc_func(bit_input)

def zfill_crc(crc:str) -> str:
    '''
    Adds leading zeros so generated crc is 8bit complementary
    '''
    bit_str = f"{crc:08b}"
    bit_str = bit_str[::-1]
    bit_str = ''.join([bit_str[i:i+8].ljust(8, '0') for i in range(0, len(bit_str), 8)])
    return bit_str[::-1]