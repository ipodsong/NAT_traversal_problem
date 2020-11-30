# parsing

### pack data ###
# pack client_ID
def pack_CID(data):
    ## data : client_ID
    ## return : 'CID:{CID}\r\n'
    return 'CID:{}\r\n'.format(data)

# pack request list from client to server
def pack_req_list(data):
    ## data : client_ID
    ## return : 'CID:{CID}\r\n'
    return 'CID:{}\r\n'.format(data)

# pack send chat
def pack_chat(data):
    ## data : [client_ID, chat contents]
    ## return 'CID:{CID}\r\nCHAT:{CHAT}\r\n'
    return 'CID:{}\r\nCHAT:{}\r\n'.format(data[0], data[1])

# pack send exit
def pack_exit(data):
    ## data : client_ID
    ## return : 'CID:{CID}\r\n'
    return 'CID:{}\r\n'.format(data)

# pack send keep alive
def pack_keep_alive(data):
    ## data : client_ID
    ## return : 'CID:{CID}\r\n'
    return 'CID:{}\r\n'.format(data)

# pack send list from server to client
def pack_res_list(data):
    ## data : [[CID1, ADDR1], [CID2, ADDR2], [CID3, ADDR3], ... ]
    ## return : 'CID:{CID1}\r\nADDR:{ADDR1}\r\nCID:{CID2}\r\nADDR:{ADDR2}\r\nCID:{CID3}\r\nADDR:{ADDR3}\r\n...'
    table = ''
    for key in data:
        ## add 'CID:{CIDi}\r\nADDR:{ADDRi}\r\n
        table = table + 'CID:{CID}\r\nADDR:{ADDR}\r\n'.format(CID=data[0], ADDR=data[1])
        
    return table

# dic for send mode
sendmode = { 0 : pack_CID, \
             1 : pack_req_list, \
             2 : pack_chat, \
             3 : pack_exit, \
             4 : pack_keep_alive, \
             5 : pack_res_list \
            }
# pack data
def make_data(mode, data):
    # mode
    # 0 : send CID
    # 1 : send req list
    # 2 : send chat
    # 3 : send keep alive
    # 4 : send exit
    # 5 : send res list
    
    # send data format
    data = 'mode:{mode}\r\n\r\n ' \
           '{data}\r\n' \
           .format(mode=mode, data=sendmode[mode](data))

    return data


### unpack data ###
# remove colon
def rmcol(data):
    # remove colon
    return data.split(':')[1]

# remove \r\n
def rmrn(data):
    return data.split('\r\n')

# unpack recv client_ID
def unpack_CID(data):
    ## data : 'CID:{CID}'
    ## return CID
    return rmcol(data)

# unpack request list from client
def unpack_req_list(data):
    ## data : 'CID:{CID}'
    ## return CID
    return rmcol(data)

# unpack sent chat from client
def unpack_chat(data):
    ## data : 'CID:{CID}\r\nCHAT:{chat}'
    ## return [CID, CHAT]
    CID, CHAT = rmrn(data)
    return [rmcol(CID), rmcol(CHAT)]

# unpack sent exit from client
def unpack_exit(data):
    ## data : 'CID:{CID}'
    ## return CID
    return rmcol(data)

# unpack sent keep alive from client
def unpack_keep_alive(data):
    ## data : 'CID:{CID}'
    ## return CID
    return rmcol(data)

# unpack sent response list from server to client
def unpack_res_list(data):
    ## data : 'CID:{CID1}\r\nADDR:{ADDR1}\r\nCID:{CID2}\r\nADDR:{ADDR2}\r\n...CID:{CIDn}\r\nADDR:{ADDRn}'
    ## return : [[CID1, ADDR1], [CID2, ADDR2], ..., [CIDn, ADDRn]]
    unpack = rmrn(data)
    unpack_list = []
    for i in range(0, len(unpack), 2):
        ##append [CIDk, ADDRk] to unpack_list, k = i/2
        unpack_list.append([rmcol(unpack[i]), rmcol(unpack[i+1])])
        
    return unpack_list

# dic for recv mode
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
    
    # split data by \r\n\r\n
    mode, data, _ = data.split('\r\n\r\n')
    
    # remove colon from 'mode:{mode}'
    mode = rmcol(mode)
    
    # unpack = dic[key = mode](arg = data)
    unpack = recvmode[mode](data)
    
    
    return int(mode), unpack

# split commend to mode and data    
def splitcmd(cmd, address):
    global client_table
    # cmd : '@commend' or '@chat [otherclient] [message]'
    splited = (cmd+' ').split(' ')
    mode = splited[0]; CID = splited[1]; msg = splited[-2]
        
    if CID in client_table:
        address = client_table[CID]
        
    return mode, address, msg