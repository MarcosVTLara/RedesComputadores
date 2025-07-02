import hashlib
import base64
import os

class SegmentFile():
    def __init__(self):
        self.buffer = {}
        self.payloadSize = 1460
        self.error_message = {'error': 'Error: The file was not found.'}

    def decode_message(self, filePath):
        file_name = os.path.basename(filePath)
        try:
            with open(filePath, 'rb') as f:
                segmentPeace = 0
                while (segment := f.read(self.payloadSize)):
                    
                    # Calcular o checksum para o pedaço
                    checksum = hashlib.md5(segment).hexdigest().encode()

                    segment_b64 = base64.b64encode(segment).decode()

                    json_packet = {
                        'checksum': checksum,
                        'segment_index': segmentPeace,
                        'data': segment_b64,
                        'is_last': False
                    }
                    if(file_name not in self.buffer):
                        self.buffer[file_name] = {
                            'segments': {}
                        }
                    self.buffer[file_name]['segments'][segmentPeace] = json_packet
                    segmentPeace += 1

            if segmentPeace > 0:
                self.buffer[file_name]['segments'][segmentPeace - 1]['is_last'] = True
                print('Last segment marked as True')

            return self.buffer[file_name]
        except FileNotFoundError:
            print(f"Error: The file '{filePath}' was not found.")
            return self.error_message
    
    def buffer_segment(self, file_name, segment_index):
        return_message = {}
        if self.buffer[file_name]['segments'][segment_index]:
            print(f'self.buffer[{file_name}].segments[{str(segment_index)}]:', self.buffer[file_name]['segments'][segment_index])
            return_message[file_name] = {
                            'segments': {}
                        }
            return_message[file_name]['segments'][segment_index] = self.buffer[file_name]['segments'][segment_index]
            return_message[file_name]['segments'][segment_index]['is_last'] = True
            return return_message[file_name]
        
        return None
    
    def error_message(self):
        return self.error_message

