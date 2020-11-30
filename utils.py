# parsing

### pack data ###
def pack_CID(data):
    ## data : client ID
    return 'CID:{}\r\n'.format(data)

def pack_req_list(data):
    ## data : client ID
    return 'CID:{}\r\n'.format(data)

def pack_chat(data):
    ## data : [client ID, chat contents]
    return 'CID:{}\r\nCHAT:{}\r\n'.format(data[0], data[1])

def pack_exit(data):
    ## data : client ID
    return 'CID:{}\r\n'.format(data)

def pack_keep_alive(data):
    ## data : client ID
    return 'CID:{}\r\n'.format(data)

def pack_res_list(data):
    ## data : [[CID1, ADDR1], [CID2, ADDR2], [CID3, ADDR3], ... ]
    table = ''
    for key in data:
        table = table + 'CID:{CID}\r\nADDR:{ADDR}\r\n'.format(CID=data[0], ADDR=data[1])
        
    return table

sendmode = { 0 : pack_CID, \
             1 : pack_req_list, \
             2 : pack_chat, \
             3 : pack_exit, \
             4 : pack_keep_alive, \
             5 : pack_res_list \
            }
def make_data(mode, data):
    # mode
    # 0 : send CID
    # 1 : send req list
    # 2 : send chat
    # 3 : send keep alive
    # 4 : send exit
    # 5 : send res list
    
    data = 'mode:{mode}\r\n\r\n ' \
           '{data}\r\n' \
           .format(mode=mode, data=sendmode[mode](data))

    return data


### unpack data ###
def rmcol(data):
    # remove colon
    return data.split(':')[1]

def rmrn(data):
    return data.split('\r\n')

def unpack_CID(data):
    ## data : 'CID:{CID}'
    ## return CID
    return rmcol(data)

def unpack_req_list(data):
    ## data : 'CID:{CID}'
    ## return CID
    return rmcol(data)

def unpack_chat(data):
    ## data : 'CID:{CID}\r\nCHAT:{chat}'
    ## return [CID, CHAT]
    CID, CHAT = rmrn(data)
    return [rmcol(CID), rmcol(CHAT)]

def unpack_exit(data):
    ## data : 'CID:{CID}'
    ## return CID
    return rmcol(data)

def unpack_keep_alive(data):
    ## data : 'CID:{CID}'
    ## return CID
    return rmcol(data)

def unpack_res_list(data):
    ## data : 'CID:{CID1}\r\nADDR:{ADDR1}\r\nCID:{CID2}\r\nADDR:{ADDR2}\r\n...CID:{CIDn}\r\nADDR:{ADDRn}'
    ## return : [[CID1, ADDR1], [CID2, ADDR2], ..., [CIDn, ADDRn]]
    unpack = rmrn(data)
    unpack_list = []
    for i in range(0,len(unpack),2):
        unpack_list.append([rmcol(unpack[i]), rmcol(unpack[i+1])])
        
    return unpack_list


recvmode = { '0' : unpack_CID, \
             '1' : unpack_req_list, \
             '2' : unpack_chat, \
             '3' : unpack_exit, \
             '4' : unpack_keep_alive, \
             '5' : unpack_res_list \
            }      
def unpack_data(data):
    # mode
    # 0 : recv CID
    # 1 : recv req list
    # 2 : recv chat
    # 3 : recv keep alive
    # 4 : recv exit
    # 5 : recv res list
    # data : 'mode:{}\r\n\r\n{DATA}\r\n\r\n'
    mode, data, _ = data.split('\r\n\r\n')
    unpack = recvmode[rmcol(mode)](data)
    
    
    return int(mode), data
