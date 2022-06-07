import base64

def fixDate(datetime, *karwgs):
    time = karwgs
    monthList = ['Janaury', 'Febaury', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    date = int(datetime.split(' ')[0].split('-')[1].split('0')[1]) -1
    if (time):
        return(f"{datetime.split(' ')[0].split('-')[2]} {monthList[date]} {datetime.split(' ')[0].split('-')[0]} {datetime.split(' ')[1]}")
    else:
        return(f"{datetime.split(' ')[0].split('-')[2]} {monthList[date]} {datetime.split(' ')[0].split('-')[0]}")

def b64Encode(string):
    b64 = base64.b64encode(string.encode('utf-8'))
    return (b64.decode('utf-8'))

def b64Decode(string):
    b64 = base64.b64decode(string.encode('utf-8'))
    return (b64.decode('utf-8'))

