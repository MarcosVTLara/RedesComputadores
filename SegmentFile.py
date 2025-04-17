import hashlib
import base64
import mimetypes
import os

class SegmentFile():
    def __init__(self):
        self.buffer = {}
        self.payloadSize = 100
        self.error_message = 'Error: The file was not found.'

    def decode_message(self, filePath):
        file_name = os.path.basename(filePath)
        try:
            with open(filePath, 'rb') as f:
                # mime_type, _ = mimetypes.guess_type(filePath)
                # file_extension = mime_type.split('/')[-1] if mime_type else 'unknown'
                # Envia os pedaços do arquivo
                segmentPeace = 0
                while (segment := f.read(self.payloadSize)):
                    
                    # Calcular o checksum para o pedaço
                    checksum = hashlib.md5(segment).hexdigest().encode()

                    segment_b64 = base64.b64encode(segment).decode()

                    json_packet = {
                        'checksum': checksum,
                        'segment_index': segmentPeace,
                        'data': segment_b64,
                        # 'typeOfFile': file_extension,
                        'is_last': False

                    }
                    if(file_name not in self.buffer):
                        self.buffer[file_name] = {
                            'segments': {}
                        }
                    self.buffer[file_name]['segments'][segmentPeace] = json_packet
                    print(f'self.buffer[{file_name}]["segments"][{segmentPeace}]:', self.buffer[file_name]['segments'][segmentPeace])
                    segmentPeace += 1

            if segmentPeace > 0:
                self.buffer[file_name]['segments'][segmentPeace - 1]['is_last'] = True
                print('Last segment marked as True')

            return self.buffer[file_name]
        except FileNotFoundError:
            print(f"Error: The file '{filePath}' was not found.")
            return self.error_message
    
    def buffer_segment(self, file_name, segment_index):
        if self.buffer[file_name].segments[segment_index]:
            print(f'self.buffer[{file_name}].segments[{segment_index}]:', self.buffer[file_name].segments[segment_index])
            return self.buffer[file_name].segments[segment_index]
        
        return None
    
    def error_message(self):
        return self.error_message

