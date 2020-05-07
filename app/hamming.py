def encode(data):
    data_bits = [int(i) for i in data]
    i = 0
    redundancy = 0
    suma = 0

    while i < len(data_bits):
        if (2**redundancy) - 1 == suma:
            redundancy += 1
        else:
            i += 1
        suma += 1

    coded = [None] * suma
    mask = 0
    redundancy = 0
    i = 0
    suma = 0
    while i < len(data):
        if (2**redundancy) - 1 == suma:
            redundancy += 1
        else:
            try:
                coded[suma] = data_bits[i]
                if data_bits[i] == 1: 
                    mask = mask ^ (suma+1)
                i+=1
            except Exception as e:
                print(str(e))
                return str(e)
        suma += 1

    redundancy = 0

    for x in range(0, suma+1):
        if 2**redundancy - 1 == x:
            if (mask & (1 << redundancy)) == 0:
                coded[x] = 0
            else:
                coded[x] = 1
            redundancy += 1
    result = ''.join(map(str, coded))
    return result