# parsing

### pack data ###
# pack client_ID
def pack_CID(data):
    ## data : [client_ID, Addr]
    ## return : 'CID:{CID}\r\nAddress:{Addr}\r\n'
    return 'CID:{}\r\nAddress:{}\r\n'.format(data[0],data[1])

# pack remove CID to client
def pack_rm_CID(data):
    ## data : [client_ID, Addr]
    ## return : 'CID:{CID}\r\nAddress:{Addr}\r\n'
    return 'CID:{}\r\nAddress:{}\r\n'.format(data[0],data[1])

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



# dic for send mode
sendmode = { 0 : pack_CID, \
             1 : pack_rm_CID, \
             2 : pack_chat, \
             3 : pack_exit, \
             4 : pack_keep_alive \
            }
# pack data
def make_data(mode, data):
    # mode
    # 0 : send create CID
    # 1 : send rm CID
    # 2 : send chat
    # 3 : send keep alive
    # 4 : send exit
    
    # send data format
    data = 'mode:{mode}\r\n\r\n' \
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

# change string to Address
def str2Addr(Addr):
    addr = Addr.replace("(","")
    addr = addr.replace(")","")
    addr = addr.replace("'","")
    addr = addr.split(", ")
    return (addr[0], int(addr[1]))

# unpack recv client_ID
def unpack_CID(data):
    ## data : 'CID:{CID}\r\nAddress:{Addr}'
    ## return CID, Addr
    CID, Addr = rmrn(data)
    return [rmcol(CID), str2Addr(rmcol(Addr))]

# unpack remove CID from server
def unpack_rm_CID(data):
    ## data : 'CID:{CID}\r\nAddress:{Addr}'
    ## return CID, Addr
    CID, Addr = rmrn(data)
    return [rmcol(CID), str2Addr(rmcol(Addr))]

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



# dic for recv mode
recvmode = { '0' : unpack_CID, \
             '1' : unpack_rm_CID, \
             '2' : unpack_chat, \
             '3' : unpack_exit, \
             '4' : unpack_keep_alive \
            }      
def unpack_data(data):
    # mode
    # 0 : recv CID
    # 1 : recv rm CID
    # 2 : recv chat
    # 3 : recv keep alive
    # 4 : recv exit
    # data : 'mode:{}\r\n\r\n{DATA}\r\n\r\n'
    
    # split data by \r\n\r\n
    mode, data, _ = data.split('\r\n\r\n')
    
    # remove colon from 'mode:{mode}'
    mode = rmcol(mode)
    
    # unpack = dic[key = mode](arg = data)
    unpack = recvmode[mode](data)
    
    
    return int(mode), unpack
