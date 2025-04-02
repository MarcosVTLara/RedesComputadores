import hashlib

def SegmentFile(filePath):
    # Geralmente, o valor do MTU padrão para Ethernet é 1500 bytes, 
    # o que inclui o cabeçalho IP e o cabeçalho UDP. O tamanho do payload UDP é 
    # tipicamente de cerca de 1472 bytes (1500 - 28 bytes para cabeçalhos IP + UDP).
    payloadSize = 100  # Definido para não ultrapassar MTU
    segmentFile = []


    with open(filePath, 'rb') as f:
        # Envia os pedaços do arquivo
        segmentPeace = 0
        while (segment := f.read(payloadSize)):
            
            # Calcular o checksum para o pedaço
            checksum = hashlib.md5(segment).hexdigest().encode()

            # Representação do número do pedaço como string
            segmentPeaceStrEncode = str(segmentPeace).encode()

            # Unir o checksum, o número do pedaço e o próprio pedaço de dados
            separator = b'|'  # Separador para dividir as partes
            packet = checksum + separator + segmentPeaceStrEncode + separator + segment
            segmentFile.append(packet)
            segmentPeace += 1

    return segmentFile
