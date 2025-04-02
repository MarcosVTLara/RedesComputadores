import os
from SegmentFile import SegmentFile
#Código da resposta + Resposta
# 0 - Extract
# 1 - Resend
# 404 - Error


def ExtractProtcol(message):
    command = message.split(" ")
    if(command[0]) == 'EXTRACT':
        transferFile = os.path.join(os.getcwd(), 'ArquivosExtract')
        transferFileFinal = os.path.join(transferFile, command[1])

        if os.path.isfile(transferFileFinal):
            return 1, SegmentFile(transferFileFinal)
            
        return 404, 'File does not exist' + command[1] + '\n'
    if(command[0]) == 'RESEND':
        if(command[1] != None):
            return 2, int(command[1])
    
    else:
        return 404, f'ERROR: The command {command[0]} does not exist'