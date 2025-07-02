import os
from SegmentFile import SegmentFile
import json

class Protcol():
    def __init__(self):
        self.segmentFile = SegmentFile()

    def read_message(self, message):
        data = json.loads(message)
        typeOfMessage = data.get('typeOfMessage').lower()
        file = data.get('file')
        segmentedIndex = data.get('segment_index')
        if typeOfMessage == 'extract':
            print('Extracting file...')
            transferFile = os.path.join(os.getcwd(), 'ArquivosExtract') # Diretorio que está os arquivos
            transferFile = os.path.join(transferFile, file) # proprio arquivo
            return self.segmentFile.decode_message(transferFile) # envio para segmentar o arquivo
        elif typeOfMessage == 'resend':
            print('Resending file...')
            return self.segmentFile.buffer_segment(file, segmentedIndex)
        elif typeOfMessage == 'close':
            return None
        else:
            return self.segmentFile.error_message()



