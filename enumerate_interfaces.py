# Use those functions to enumerate all interfaces available on the system using Python.
# found on <http://code.activestate.com/recipes/439093/#c1>

import socket
import fcntl
import struct
import array

def all_interfaces():
    max_possible = 128  # arbitrary. raise if needed.
    bytes = max_possible * 32
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', b'\0' * bytes)
    outbytes = struct.unpack('iL', fcntl.ioctl(
        s.fileno(),
        0x8912,  # SIOCGIFCONF
        struct.pack('iL', bytes, names.buffer_info()[0])
    ))[0]
    namestr = names.tostring()
    lst = []
    for i in range(0, outbytes, 40):
        name = namestr[i:i+16].split(b'\0', 1)[0]
        ip   = namestr[i+20:i+24]
        lst.append((name.decode('utf-8'), ip))
    return lst

def format_ip(addr):
    return str(addr[0]) + '.' + \
           str(addr[1]) + '.' + \
           str(addr[2]) + '.' + \
           str(addr[3])

#ifs = all_interfaces()
#for i in ifs:
#    print("%12s   %s" % (i[0], format_ip(i[1])))