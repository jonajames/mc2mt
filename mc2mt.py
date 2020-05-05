#!/usr/bin/python

import os
import time
import argparse
import sqlite3
import queue
import threading

from block_conversion import convertBlock
from section_conversion import convertSection
from blob_writer import writeBlob

from quarry.types.nbt import RegionFile
from quarry.types.registry import OpaqueRegistry
from quarry.types.chunk import BlockArray

def mcaIterator(mca_file,registry):
    with RegionFile(mca_file) as region_file:
        for chunk_x in range(0,32):
            for chunk_z in range(0,32):
                for chunk_y in range(0,16):
                    try: chunk,section = region_file.load_chunk_section(chunk_x,chunk_y,chunk_z)
                    except ValueError as e: continue
                    try: blocks = BlockArray.from_nbt(section,registry)
                    except KeyError as e: continue
                    yield {
                        'mca' : mca_filename,
                        'x' : chunk_x,
                        'z' : chunk_z,
                        'y' : chunk_y,
                        'blocks' : blocks,
                    }

def conversionWorker(mca_file_queue,converted_section_queue):
    convert_block_function = convertBlock
    registry = OpaqueRegistry(2048)
    work_time = 0
    try:
        while True:
            mca_file = mca_file_queue.get(timeout=5)
            for found_section in mcaIterator(mca_file,registry):
                converted_section = convertSection(found_section,convert_block_function)
                pos = converted_section['pos']
                blob = writeBlob(converted_section)
                work_time += time.time() - start_time
                converted_section_queue.put((pos,blob))
            print("Conversion",mca_file,"ended")
    except queue.Empty:
        pass

def databaseWorker(output_map_path,converted_section_queue):
    connection = sqlite3.connect(output_map_path+"/map.sqlite")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `blocks` (`pos` INT NOT NULL PRIMARY KEY, `data` BLOB);")
    num_saved = 0
    try:
        while True:
            pos,blob = converted_section_queue.get(timeout=5)
            try: cursor.execute("INSERT INTO blocks VALUES (?,?)",(pos,blob))
            except sqlite3.IntegrityError:
                print(f"Duplicate Chunk: {pos:X} of size: {len(blob)}");
                continue
            print(f"Blocks saved:",num_saved,end="\r")
            num_saved += 1
            if num_saved%128 == 0: connection.commit()
    except queue.Empty:
        connection.commit()
        connection.close()
        print("All",num_saved,"blocks saved!")

if __name__ == '__main__':
    # Parse args
    parser = argparse.ArgumentParser(description='Convert maps from Minecraft to Minetest.',epilog="""
    More details at https://quarry.readthedocs.io/en/latest/data_types/registry.html
    """)
    parser.add_argument('input',help='Minecraft input world folder')
    parser.add_argument('output',help='Output folder for the generated world. Must not exist.')
    parser.add_argument("--threads","-t",type=int,default=1,help="Number of worker threads")
    args = parser.parse_args()
    
    # Create world structure
    os.makedirs(args.output)
    with open(args.output+"/world.mt",'w') as world_mt:
        world_mt.write(
            "enable_damage = false\n" +\
            "creative_mode = true\n" +\
            "gameid = minetest\n" +\
            "backend = sqlite3\n" +\
            "auth_backend = sqlite3\n" +\
            "player_backend = sqlite3\n" +\
            "")
    os.makedirs(args.output+"/worldmods/mc2mt")
    with open(args.output+"/worldmods/mc2mt/init.lua",'w') as map_meta:
        map_meta.write(
            'minetest.set_mapgen_params({water_level = -2})\n' +\
            'minetest.set_mapgen_params({chunksize = 1})\n' +\
            'minetest.set_mapgen_params({mgname = "singlenode"})\n' +\
            'minetest.register_on_generated(function(minp, maxp, seed)\n' +\
            '        local vm = minetest.get_voxel_manip(minp, maxp)\n' +\
            '        vm:calc_lighting(minp, maxp)\n' +\
            '        vm:set_lighting({day = 15, night = 0}, minp, maxp)\n' +\
            '        vm:update_liquids()\n' +\
            '        vm:write_to_map()\n' +\
            'end)\n' +\
            "")
        
    # Database worker
    converted_section_queue = queue.Queue(10*args.threads)
    database_worker =  threading.Thread(
        name = "database_worker",
        target=databaseWorker,
        args=(args.output,converted_section_queue))
    database_worker.start()

    # Conversion worker
    start_time = time.time()
    num_mca = len(os.listdir(args.input+"/region"))
    mca_filenames =  os.listdir(args.input+"/region")
    mca_file_queue = queue.Queue(args.threads)
    conversion_workers = []
    print("Beginning conversion with",args.threads,"workers")
    for i in range(args.threads):
        conversion_worker = threading.Thread(
            name = f"conversion_worker_{1}",
            target = conversionWorker,
            args = (mca_file_queue,converted_section_queue)
        )
        conversion_worker.start()
        conversion_workers.append(conversion_worker)
    for mca_filename in mca_filenames:
        mca_file_queue.put(args.input+"/region/"+mca_filename)
        
    # End
    for conversion_worker in conversion_workers: conversion_worker.join()
    database_worker.join()
    elapsed_time = ( time.time()-start_time ) / 60 
    print("Conversion ended in",f"{elapsed_time:.02f}")
