from . import block_conversion

def coord(z,y,x):
    return (z<<8) | (y<<4) | x

def convert_section(
        filename,
        chunk_x,
        chunk_z,
        section_y,
        chunk
):
    converted_itemstring = {}
    converted_section = {
        'pos' : (0,0,0),
        'param0' : [0]*4096,
        'param1' : [255]*4096,
        'param2' : [0]*4096,
        'mappings' : [],
    }

    # Convert block coordinates
    r,region_x,region_z,mca = filename.split(".")
    x = (-int(region_x) << 5) | (31-chunk_x) # X axis is flipped
    z = ( int(region_z) << 5) | (chunk_z)
    converted_section["pos"] = (x,section_y,z)

    # Loop on all blocks
    count = 0
    section = chunk.get_section(section_y)
    if not section: return

    for block in chunk.stream_blocks(0,section_y,True):
        y = count // 256
        z = count // 16 % 16
        x = - count % 16
        count += 1
        itemstring,param1,param2 = block_conversion.convert_block(block)
        if itemstring not in converted_itemstring:
            converted_section["mappings"].append(itemstring)
            index = converted_section["mappings"].index(itemstring)
            converted_itemstring[itemstring] = index
        param0 = converted_itemstring[itemstring]
        converted_section["param0"][coord(z,y,x)] = param0
        converted_section["param1"][coord(z,y,x)] = param1
        converted_section["param2"][coord(z,y,x)] = param2

    # End
    return converted_section
