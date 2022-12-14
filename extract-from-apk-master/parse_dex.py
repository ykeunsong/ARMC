import struct

def isdex(mm):
    if mm[0:3] == 'dex' and len(mm) > 0x70:
        return True

    return False

def header(mm) :
    magic = mm[0:8]
    checksum = struct.unpack('<L', mm[8:0xC])[0]
    sa1 = mm[0xC:0x20]
    file_size = struct.unpack('<L', mm[0x20:0x24])[0]
    header_size = struct.unpack('<L', mm[0x24:0x28])[0]
    endian_tag = struct.unpack('<L', mm[0x28:0x2C])[0]
    link_size = struct.unpack('<L', mm[0x2C:0x30])[0]
    link_off = struct.unpack('<L', mm[0x30:0x34])[0]
    map_off = struct.unpack('<L', mm[0x34:0x38])[0]
    string_ids_size = struct.unpack('<L', mm[0x38:0x3C])[0]
    string_ids_off = struct.unpack('<L', mm[0x3C:0x40])[0]
    type_ids_size = struct.unpack('<L', mm[0x40:0x44])[0]
    type_ids_off = struct.unpack('<L', mm[0x44:0x48])[0]
    proto_ids_size = struct.unpack('<L', mm[0x48:0x4C])[0]
    proto_ids_off = struct.unpack('<L', mm[0x4C:0x50])[0]
    field_ids_size = struct.unpack('<L', mm[0x50:0x54])[0]
    field_ids_off = struct.unpack('<L', mm[0x54:0x58])[0]
    method_ids_size = struct.unpack('<L', mm[0x58:0x5C])[0]
    method_ids_off = struct.unpack('<L', mm[0x5C:0x60])[0]
    class_defs_size = struct.unpack('<L', mm[0x60:0x64])[0]
    class_defs_off = struct.unpack('<L', mm[0x64:0x68])[0]
    data_size = struct.unpack('<L', mm[0x68:0x6C])[0]
    data_off = struct.unpack('<L', mm[0x6C:0x70])[0]
    hdr = {}

    if len(mm) != file_size:
        return hdr

    hdr['magic' ] = magic
    hdr['checksum' ] = checksum
    hdr['sa1' ] = sa1
    hdr['file_size' ] = file_size
    hdr['header_size' ] = header_size
    hdr['endian_tag' ] = endian_tag
    hdr['link_size' ] = link_size
    hdr['link_off' ] = link_off
    hdr['map_off' ] = map_off
    hdr['string_ids_size'] = string_ids_size
    hdr['string_ids_off' ] = string_ids_off
    hdr['type_ids_size' ] = type_ids_size
    hdr['type_ids_off' ] = type_ids_off
    hdr['proto_ids_size' ] = proto_ids_size
    hdr['proto_ids_off' ] = proto_ids_off
    hdr['field_ids_size' ] = field_ids_size
    hdr['field_ids_off' ] = field_ids_off
    hdr['method_ids_size'] = method_ids_size
    hdr['method_ids_off' ] = method_ids_off
    hdr['class_defs_size'] = class_defs_size
    hdr['class_defs_off' ] = class_defs_off
    hdr['data_size' ] = data_size
    hdr['data_off' ] = data_off

    return hdr

def string_id_list(mm, hdr):
    string_id = []
    string_ids_size = hdr['string_ids_size']
    string_ids_off = hdr['string_ids_off']

    for i in range(string_ids_size):
        off = struct.unpack('<L', mm[string_ids_off+(i*4): string_ids_off+(i*4)+4])[0]
        c_size = ord(mm[off])
        c_char = mm[off+1:off+1+c_size]
        string_id.append(c_char)

    return string_id

def method_id_list(mm, hdr):
    method_list = []

    method_ids_size = hdr['method_ids_size']
    method_ids_off = hdr['method_ids_off']
    for i in range(method_ids_size):
        class_idx = struct.unpack('<H', mm[method_ids_off+(i*8): method_ids_off+(i*8)+2])[0]
        proto_idx = struct.unpack('<H', mm[method_ids_off+(i*8)+2: method_ids_off+(i*8)+4])[0]
        name_idx = struct.unpack('<L', mm[method_ids_off+(i*8)+4: method_ids_off+(i*8)+8])[0]
        method_list.append([class_idx, proto_idx, name_idx])

    return method_list

def type_id_list(mm, hdr):
    type_list = []

    type_ids_size = hdr['type_ids_size']
    type_ids_off = hdr['type_ids_off']

    for i in range(type_ids_size):
        idx = struct.unpack('<L', mm[type_ids_off+(i*4):type_ids_off+(i*4)+4])[0]
        type_list.append(idx)

    return type_list
