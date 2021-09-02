#!/usr/bin/python
import os
import time

import anvil

from mc2mtlib import *

# Main
if __name__ == '__main__':

    # Args
    args = parse_args()
    if args.disable_all_mods:
        for mod in block_conversion.mods_enabled:
            block_conversion.mods_enabled[mod] = False
    if args.enable_all_mods:
        for mod in block_conversion.mods_enabled:
            block_conversion.mods_enabled[mod] = True
    for mod in block_conversion.mods_enabled:
        if args.__dict__.get('disable_'+mod,False):
            block_conversion.mods_enabled[mod] = False
        if args.__dict__.get('enable_'+mod,False):
            block_conversion.mods_enabled[mod] = True
    if args.unknown_as_air:
        block_conversion.unknown_as_air = True
    if args.quiet:
        block_conversion.report_unknown_blocks = False
    if args.mod:
            for mod_file in args.mod:
                block_conversion.load_mod(mod_file)

    print("Mods enabled in this order:")
    for p,mod in block_conversion.mods_priority:
        if block_conversion.mods_enabled[mod]: print(p,mod)
    print()

    # Conversion
    print("Starting Conversion:")
    start_time = time.time()
    world = minetest_world.MinetestWorld(args.output)
    mca_files = os.listdir(os.path.join(args.input,"region"))
    mca_files = [f for f in mca_files if f[-4:]==".mca" ]
    cnt_files = 0
    for mca_file in mca_files:
        cnt_files += 1
        mca_path = os.path.join(args.input,"region",mca_file)
        print("Converting",mca_file,"file",cnt_files,"of",len(mca_files))
        region = anvil.Region.from_file(mca_path)
        for chunk_x in range(0,32):
            for chunk_z in range(0,32):
                try: chunk = region.get_chunk(chunk_x,chunk_z)
                except anvil.errors.ChunkNotFound: continue
                for section_y in range(0,16):
                    converted = section_conversion.convert_section(
                        mca_file,
                        chunk_x,
                        chunk_z,
                        section_y,
                        chunk
                    )
                    if not converted: continue
                    world.insert(converted)
                print(f"Map Blocks saved: {world.saved_map_block}",end="\r")
    # End
    world.save()
    if world.saved_map_block:
        print(f"Map Blocks saved: {world.saved_map_block}",end="\n")
    else:
        print("No blocks have been saved. Map version is not supported?")
    print(f"Conversion ended in {(time.time()-start_time)/60:.02f} m")
