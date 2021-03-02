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
    converted_blocks = {}
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

    # Convert palette
    try:
        palette = chunk.get_palette(section_y);
    except:
        palette = False
    if not palette:
        return
    else:
        for block in palette:
            converted_blocks[block] = block_conversion.convert_block(block)
        for block in converted_blocks:
            itemstring,param1,param2 = converted_blocks[block]
            if itemstring not in converted_itemstring:
                converted_section["mappings"].append(itemstring)
            index = converted_section["mappings"].index(itemstring)
            converted_itemstring[itemstring] = index

    #for k in converted_blocks: print(k,converted_blocks[k])
            
    # Loop on all blocks
    for y in range(16):
        for z in range(16):
            for x in range(16):
                global_y = (section_y << 4) | y
                block = chunk.get_block(15-x,global_y,z,None,True)
                itemstring,param1,param2 = converted_blocks[block]
                param0 = converted_itemstring[itemstring]
                converted_section["param0"][coord(z,y,x)] = param0
                converted_section["param1"][coord(z,y,x)] = param1
                converted_section["param2"][coord(z,y,x)] = param2

    # End
    return converted_section
