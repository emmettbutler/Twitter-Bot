def read_image(filename):
    bytes = []
    f = open(filename, "rb")
    try:
        byte = f.read(1)
        while byte != "":
            bytes.append(byte)
            byte = f.read(1)
    finally:
        f.close()
    return bytes

def group_by_threes(bytes):
    threes = []
    count = 0
    for byte in bytes:
        if count % 3 == 0:
            threes.append((bytes[bytes.index(byte)], bytes[bytes.index(byte)+1], bytes[bytes.index(byte)+2]))
        count += 1
    return threes

def change_color(threes, old_color, new_color):
    for item in threes:
        if item[0] == old_color[0] and item[1] == old_color[1] and item[2] == old_color[2]:
            threes[threes.index(item)] = (new_color[0], new_color[1], new_color[2])
    return threes

def write_bmp(filename, threes):
    new = open(filename, "w")
    for item in threes:
        for byte in item:
            new.write(byte)
    new.close()

if __name__ == "__main__":
    threes = group_by_threes(read_image("bitmap.bmp"))
    new = change_color(threes, (b'\x00', b'\x00', b'\x00'), (b'\xff', b'\xff', b'\x00'))
    write_bmp("new.bmp", new)
