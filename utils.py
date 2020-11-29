# parsing

def make_data(mode, data):
    # mode
    # 0 : send CID
    # 1 : request list
    # 2 : send chat
    # 3 : send keep alive
    data = 'mode:{mode}\r\n ' \
           'data:{data}' \
           .format(mode=mode, data=data)

    return data
